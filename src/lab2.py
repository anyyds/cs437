import picar_4wd as fc
import numpy as np
import math

obstacle_grid = np.zeros((100, 100))

def mark_obstacle(grid, x, y):
    if 0 <= x < 100 and 0 <= y < 100:
        grid[y, x] = 1

def scan_surroundings():
    for angle_deg in range(-60, 60, 5):
        # set servo angle
        fc.servo.set_angle(angle_deg)
        fc.time.sleep(0.05)
        # get distance in cm
        dist = fc.us.get_distance()
        if dist < 0:
            continue
        
        x = int(round(dist * math.cos(math.radians(angle_deg))))
        y = int(round(dist * math.sin(math.radians(angle_deg))))

        mark_obstacle(obstacle_grid, x, y + 49)

def main():
    scan_surroundings()
    print(obstacle_grid)

if __name__ == "__main__":
    main()