import picar_4wd as fc
import time
import random

speed = 30
min_dist = 20

def main():
    while True:
        # dist = fc.us.get_distance()
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue
        # if dist > 0 and dist < min_dist:
        if scan_list[3:7] != [2, 2, 2, 2]:
            fc.stop()
            direction = random.choice([1, 2]) # 1 = left, 2 = right
            turn_time = random.uniform(0.6, 1.5)
            fc.backward(speed)
            time.sleep(0.3)
            if direction == 1:
                fc.turn_left(speed)
            else:
                fc.turn_right(speed)
            time.sleep(turn_time)
            fc.stop()
        else:
            fc.forward(speed)
        time.sleep(0.1)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by ^C")
    finally:
        fc.stop()