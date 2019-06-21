import threading
import os


class Traverse(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        try:
            for root, dirs, files in os.walk(self.path, topdown=True):
                print("there are", len(files), "files in", root)
                for each_file in files:
                    print (each_file)
        except Exception as e:
            print(e)
        return


folders = ["C:\\Users", "C:\\Program Files"]
for path in folders:
    files = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]
    directories = [d for d in os.listdir(
        path) if os.path.isdir(os.path.join(path, d))]
    for f in files:
        print(f, path)
    for path in directories:
        thread = Traverse(path)
        thread.start()
