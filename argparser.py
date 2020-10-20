#-*-coding:cp1254-*-
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--data",    help = "Give the argument that you want to count eggs on. If you want to use your camera give 'livefeed' as an argument or if you want to count the eggs of a video type videos name.  ")
    result = parser.parse_args()
    data   = result.data
    try:
        data  = int(data)
    except ValueError as err:
        pass

    return data

