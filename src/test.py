import picar_4wd as fc
import time

def main():
    # dist = fc.get_distance_at(0)
    # print(dist)

    fc.turn_left(20)

    time.sleep(1)

    fc.stop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by ^C")
    finally:
        fc.stop()