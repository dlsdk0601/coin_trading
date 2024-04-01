from src.upbit import UpbitData


def main():
    upbit = UpbitData()

    upbit.run()
    # while True:
    #     upbit.run()
    #     time.sleep(secs=10)


if __name__ == '__main__':
    main()
