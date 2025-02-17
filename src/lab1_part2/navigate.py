import time
import math
import numpy as np
import picar_4wd as fc
import ultrasonic_detect
from plan_path import plan_path
from detect_stop_sign import StopSignDetector

import heapq


def navigate_path(path, cur_orientation, cur_pos, stop_sign_detector):
    if not path:
        print("No valid path.")
        return

    turned = False
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
            return True
        elif diff == 2:
            turn_around()
            return True
        elif diff == 3:
            turn_left()
            return True
        return False

    # Move cell by cell
    for i in range(len(path) - 1):
        (x1, y1) = path[i]
        (x2, y2) = path[i + 1]
        dx = x2 - x1
        dy = y2 - y1
        if dx == -1 and dy == 0:
            turned = turn_to('E', cur_orientation)
            cur_orientation = 'E'
        elif dx == 1 and dy == 0:
            turned = turn_to('W', cur_orientation)
            cur_orientation = 'W'
        elif dx == 0 and dy == -1:
            turned = turn_to('S', cur_orientation)
            cur_orientation = 'S'
        elif dx == 0 and dy == 1:
            turned = turn_to('N', cur_orientation)
            cur_orientation = 'N'
        else:
            print(f"Error: Invalid step from {(x1,y1)} to {(x2,y2)}")
            break
        if turned:
            break
        fc.forward(5)
        time.sleep(0.5)
        fc.stop()
        cur_pos = (x2, y2)
    return cur_orientation, cur_pos

def main():
    cur_pos = (9, 0)
    destination = (9, 19)
    cur_orientation = 'N'
    grid_size = 20
    stop_sign_detector = StopSignDetector()
    while True:
        obstacle_grid = ultrasonic_detect.scan_surroundings(
            cur_pos=cur_pos,
            cur_orientation=cur_orientation,
            grid_size=grid_size
        )
        log = obstacle_grid.copy()
        log[cur_pos] = 2
        log[destination] = 3
        print("Obstacle Grid:\n", log)
        print("Current orientation: ", cur_orientation)
        path = plan_path(obstacle_grid, cur_pos, destination)
        if not path:
            print("No valid path found")
            break
        while stop_sign_detector.run():
            time.sleep(0.1)
        cur_orientation, cur_pos = navigate_path(path[:2], cur_orientation, cur_pos, stop_sign_detector)
        if cur_pos == destination:
            print("reached destination")
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