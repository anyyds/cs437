import time
import math
import numpy as np
import picar_4wd as fc
import ultrasonic_detect
import plan_path

import heapq


def navigate_path(path, cell_size=20, move_time=0.5):
    if not path or len(path) < 2:
        print("No valid path or path too short to navigate.")
        return

    orientation = 'N'

    def turn_to(target_orientation):
        nonlocal orientation
        order = ['N', 'E', 'S', 'W']
        current_idx = order.index(orientation)
        target_idx = order.index(target_orientation)
        diff = (target_idx - current_idx) % 4
        if diff == 1:
            fc.turn_right(20)
            time.sleep(1.1)
            fc.stop()
        elif diff == 2:
            fc.turn_right(20)
            time.sleep(2.2)
            fc.stop()
        elif diff == 3:
            fc.turn_left(20)
            time.sleep(1.1)
            fc.stop()
        orientation = target_orientation

    # Move cell by cell
    for i in range(len(path) - 1):
        (x1, y1) = path[i]
        (x2, y2) = path[i + 1]
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1 and dy == 0:
            turn_to('E')
        elif dx == -1 and dy == 0:
            turn_to('W')
        elif dx == 0 and dy == 1:
            turn_to('S')
        elif dx == 0 and dy == -1:
            turn_to('N')
        else:
            print(f"Warning: Invalid step from {(x1,y1)} to {(x2,y2)}")
            continue
        fc.forward(5)
        time.sleep(1)
        fc.stop()

    print("Navigation complete.")


if __name__ == "__main__":
    test_grid = np.array([
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    start_coord = (4, 2)
    dest_coord = (0, 0)

    result_path = plan_path(test_grid, start_coord, dest_coord)
    if result_path is None:
        print("No path found.")
    else:
        print("Path found:", result_path)
        navigate_path(result_path)
