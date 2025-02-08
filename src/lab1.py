import picar_4wd as fc

def main():
    while True:
        if fc.get_distance_at(0) > 8:
            fc.forward(30)
        else:
            fc.stop()


if __name__ == '__main__':
    try:
        main()
    finally:
        fc.stop()