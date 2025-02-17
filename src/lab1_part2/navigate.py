import time
import math
import numpy as np
import picar_4wd as fc
import ultrasonic_detect
from plan_path import plan_path

import heapq


def navigate_path(path, cur_orientation, cur_pos):
    if not path:
        print("No valid path.")
        return

    def turn_right():
        fc.turn_right(20)
        time.sleep(1.1)
        fc.stop()
    def turn_left():
        fc.turn_left(20)
        time.sleep(1.1)
        fc.stop()
    def turn_around():
        fc.turn_right(20)
        time.sleep(2.2)
        fc.stop()
    def turn_to(target_orientation, cur_orientation): # turn to one of N, E, S, W
        order = ['N', 'E', 'S', 'W']
        current_idx = order.index(cur_orientation)
        target_idx = order.index(target_orientation)
        diff = (target_idx - current_idx) % 4
        if diff == 1:
            turn_right()
        elif diff == 2:
            turn_around()
        elif diff == 3:
            turn_left()

    # Move cell by cell
    for i in range(len(path) - 1):
        (x1, y1) = path[i]
        (x2, y2) = path[i + 1]
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1 and dy == 0:
            turn_to('E', cur_orientation)
            cur_orientation = 'E'
        elif dx == -1 and dy == 0:
            turn_to('W', cur_orientation)
            cur_orientation = 'W'
        elif dx == 0 and dy == 1:
            turn_to('S', cur_orientation)
            cur_orientation = 'S'
        elif dx == 0 and dy == -1:
            turn_to('N', cur_orientation)
            cur_orientation = 'N'
        else:
            print(f"Error: Invalid step from {(x1,y1)} to {(x2,y2)}")
            break
        fc.forward(5)
        time.sleep(1)
        fc.stop()
        cur_pos = (x2, y2)

    print("Navigation complete.")
    return cur_orientation, cur_pos

def main():
    cur_pos = (3, 6)
    destination = (0, 0)
    cur_orientation = 'N'
    grid_size = 7
    obstacle_grid = np.zeros((grid_size, grid_size), dtype=int)
    while True:
        obstacle_grid = ultrasonic_detect.scan_surroundings(
            obstacle_grid,
            cur_pos=cur_pos,
            cur_orientation=cur_orientation,
            grid_size=grid_size
        )
        print("Obstacle Grid:\n", obstacle_grid)
        path = plan_path(obstacle_grid, cur_pos, destination)
        cur_orientation, cur_pos = navigate_path(path[:5], cur_orientation, cur_pos)
        if cur_pos == destination:
            break

    return


if __name__ == "__main__":
    # test_grid = np.array([
    #     [0, 0, 1, 0, 0],
    #     [0, 1, 0, 1, 1],
    #     [0, 0, 0, 0, 0],
    #     [1, 1, 1, 0, 0],
    #     [0, 0, 0, 0, 0]
    # ])
    # start_coord = (2, 4)
    # dest_coord = (0, 0)

    # result_path = plan_path(test_grid, start_coord, dest_coord)
    # if result_path is None:
    #     print("No path found.")
    # else:
    #     print("Path found:", result_path)
    #     navigate_path(result_path)
    main()