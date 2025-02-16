import picar_4wd as fc
import numpy as np
import math

size = 100

obstacle_grid = np.zeros((size, size))

def mark_obstacle(grid, x, y, clearance = 2):
    for i in range(x - clearance, x + clearance + 1):
        for j in range(y - clearance, y + clearance + 1):
            if 0 <= i < size and 0 <= j < size:
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

        mark_obstacle(obstacle_grid, x, y + (size / 2 - 1))

def main():
    scan_surroundings()
    print(obstacle_grid)

if __name__ == "__main__":
    main()