import picar_4wd as fc
import numpy as np
import math

def mark_obstacle(grid, grid_size, x, y, clearance = 1):
    x = int(x)
    y = int(y)
    for i in range(x - clearance, x + clearance + 1):
        for j in range(y - clearance, y + clearance + 1):
            if 0 <= i < grid_size and 0 <= j < grid_size:
                grid[j, i] = 1

def scan_surroundings(cur_pos = (19,39), cur_orientation = 'N', grid_size = 40):
    cur_x, cur_y = cur_pos
    # get angle offset from orientation
    if cur_orientation == 'E':
        angle_offset = -90
    elif cur_orientation == 'S':
        angle_offset = 180
    elif cur_orientation == 'W':
        angle_offset = 90
    else:
        angle_offset = 0
    obstacle_grid = np.zeros((grid_size, grid_size))
    for angle_deg in range(-60, 60, 5):
        # set servo angle
        fc.servo.set_angle(angle_deg)
        fc.time.sleep(0.05)
        abs_angle_deg = angle_offset + angle_deg
        # get distance in cm
        dist = fc.us.get_distance()
        if dist < 0:
            continue
        
        x = int(round(dist/10 * math.cos(math.radians(angle_deg)))) + cur_x
        y = int(round(dist/10 * math.sin(math.radians(angle_deg)))) + cur_y

        mark_obstacle(obstacle_grid, grid_size, x, y + (grid_size // 2 - 1))
    return obstacle_grid

def main():
    obstacle_grid = scan_surroundings(cur_pos=(2, 4), cur_orientation='N', grid_size=5)
    print(obstacle_grid)

if __name__ == "__main__":
    main()