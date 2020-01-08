import os.path
import argparse


def main(path):
    if os.path.isfile(path):
        with open(path, "r") as fp:
            data = fp.readlines()
        for index, line in enumerate(data):
            if "traceback.format_" in line:
                data[index] = data[index].replace("error", "debug").replace("info", "debug").replace("warn", "debug")
        with open(path, "w") as fp:
            fp.write("".join(data))
        return 0
    else:
        print("Invalid file path")
        return -1


if __name__=="__main__":
    import sys
    parser = argparse.ArgumentParser(description="Update blusapphire services")
    parser.add_argument("--path", type=str, default="", help="path of the file")
    args = parser.parse_args()
    if args.path:
        sys.exit(main(args.path))
    else:
        print("No arguments provided")
        sys.exit(-1)

