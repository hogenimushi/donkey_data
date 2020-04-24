import sys
import shutil
import os
import json


class TrimmingData:
    def __init__(self, current_dir, first_num, last_num, target_dir):
        self.current_img_path = current_dir + "/{}_cam-image_array_.jpg"
        self.current_json_path = current_dir + "/record_{}.json"
        self.first_num = first_num
        self.last_num = last_num
        self.target_img_path = target_dir + "/{}_cam-image_array_.jpg"
        self.target_json_path = target_dir + "/record_{}.json"
        self.count = 1

    def copy_data(self):
        print("copying data ...")
        for i in range(self.first_num, self.last_num):
            shutil.copyfile(self.current_img_path.format(i), self.target_img_path.format(self.count))
            shutil.copyfile(self.current_json_path.format(i), self.target_json_path.format(self.count))
            with open(self.target_json_path.format(self.count), 'r') as f:
                tmp = json.load(f)
                tmp["cam/image_array"] = "{}_cam-image_array_.jpg".format(self.count)
            with open(self.target_json_path.format(self.count), 'w') as f:
                json.dump(tmp, f)
            self.count += 1
        print(" finishing trimming and copy data!")


def verification_data(path):
    print("checking " + path + " ... ", end="")
    if os.path.exists(path + "/meta.json"):
        print("ok")
    else:
        print("\n" + path + " doesn't exist donkey data.")
        exit(1)


def verification_target_dir(path):
    print("checking destination data path ... ", end="")
    if os.path.exists(path):
        print("ok")
    else:
        os.mkdir(path)
        print("doesn't exist destination directory, making dir: " + path)


def main(current_dir, first_num, last_num, target_dir):
    print("source data path: " + current_dir)
    print("first record number: " + str(first_num))
    print("last record number: " + str(last_num))
    print("destination data path: " + target_dir)
    verification_data(current_dir)
    verification_target_dir(target_dir)
    trim = TrimmingData(current_dir, first_num, last_num, target_dir)
    trim.copy_data()


if __name__ == '__main__':
    args = sys.argv
    current_path = args[1]
    first = int(args[2])
    last = int(args[3])
    target_path = args[4]
    main(current_path, first, last, target_path)