import os
import json
import numpy as np
from argparse import ArgumentParser


class ChangeFreqImg:
    def __init__(self, path, current_freq, target_freq):
        self.path = path
        self.img_path = path + "/{}_cam-image_array_.jpg"
        self.data_num = []
        self.each_num = int(current_freq / target_freq)
        self.count = 1

    def remake_img(self):
        print("changing image frequency ...")
        for i in self.data_num:
            if self.count < self.each_num:
                os.remove(self.img_path.format(i))
                self.count += 1
            else:
                os.rename(self.img_path.format(i), self.img_path.format(int(i / self.each_num)))
                self.count = 1


class ChangeFreqJson:
    def __init__(self, path, current_freq, target_freq):
        self.path = path
        self.record_path = path + "/record_{}.json"
        self.data_num = []
        self.angle = 0
        self.throttle = 0
        self.each_num = int(current_freq / target_freq)
        self.count = 1

    def remake_json(self):
        print("changing json frequency ...")
        for i in self.data_num:
            with open(self.record_path.format(i), 'r') as f:
                tmp = json.load(f)
                self.angle += float(tmp["user/angle"])
                self.throttle += float(tmp["user/throttle"])
            if self.count < self.each_num:
                os.remove(self.record_path.format(i))
                self.count += 1
            else:
                tmp["user/angle"] = self.angle/self.each_num
                tmp["user/throttle"] = self.throttle/self.each_num
                tmp["cam/image_array"] = "{}_cam-image_array_.jpg".format(int(i/self.each_num))
                with open(self.record_path.format(int(i/self.each_num)), 'w') as f:
                    json.dump(tmp, f)
                os.remove(self.record_path.format(i))
                self.angle = 0
                self.throttle = 0
                self.count = 1


class ApproximateChangeFreqJson:
    def __init__(self, path, current_freq, target_freq):
        self.path = path
        self.record_path = path + "/record_{}.json"
        self.data_num = []
        self.angle = []
        self.throttle = []
        self.each_num = int(current_freq / target_freq)
        self.app_block = int(current_frequency/4)

    def remake_json(self):
        print("changing json frequency ...")
        for i in self.data_num:
            with open(self.record_path.format(i), 'r') as f:
                tmp = json.load(f)
                self.angle.append(float(tmp["user/angle"]))
                self.throttle.append(float(tmp["user/throttle"]))
        pre = 1
        for i in self.data_num[self.app_block:(-1*self.app_block):self.each_num]:
            for j in range(pre, i):
                os.remove(self.record_path.format(j))
            pre = i+1
            res_angle = np.polyfit(self.data_num[i-self.app_block:i+self.app_block],
                                   self.angle[i-self.app_block:i+self.app_block], 3)
            res_throttle = np.polyfit(self.data_num[i-self.app_block:i+self.app_block],
                                      self.throttle[i-self.app_block:i+self.app_block], 3)
            with open(self.record_path.format(i), 'r') as f:
                tmp = json.load(f)
                tmp["user/angle"] = np.poly1d(res_angle)(self.data_num[i])
                tmp["user/throttle"] = np.poly1d(res_throttle)(self.data_num[i])
                tmp["cam/image_array"] = "{}_cam-image_array_.jpg".format(int((i-self.app_block)/self.each_num)+1)
            with open(self.record_path.format(int((i-self.app_block)/self.each_num)+1), 'w') as f:
                json.dump(tmp, f)
            os.remove(self.record_path.format(i))
        for i in self.data_num[(-1*self.app_block):]:
            os.remove(self.record_path.format(i))


def verification_data(path):
    print("checking " + path + " ... ", end="")
    if os.path.exists(path + "/meta.json"):
        print("ok")
        return
    else:
        print("\n" + path + "doesn't exist donkey data.")
        exit(1)


def make_data_list(path):
    count = 1
    num = []
    print("making data list ...")
    while True:
        if os.path.exists(path.format(count)):
            num.append(count)
            count += 1
        else:
            return num


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--current', type=int, default=20, help="current_frequency")
    argparser.add_argument('--target', type=int, default=10, help="target_frequency")
    argparser.add_argument('--tub', type=str, help="tab_path")
    argparser.add_argument('--test', action='store_true', help="if using test mode, --test option")
    return argparser.parse_args()


def main():
    verification_data(file_path)
    i = ChangeFreqImg(file_path, current_frequency, target_frequency)
    i.data_num = make_data_list(i.img_path)
    i.remake_img()
    j = ChangeFreqJson(file_path, current_frequency, target_frequency)
    j.data_num = i.data_num
    j.remake_json()
    print("finish changing frequency!")


def test():
    verification_data(file_path)
    i = ChangeFreqImg(file_path, current_frequency, target_frequency)
    i.data_num = make_data_list(i.img_path)
    i.remake_img()
    j = ApproximateChangeFreqJson(file_path, current_frequency, target_frequency)
    j.data_num = i.data_num
    j.remake_json()
    print("finish changing frequency!")


if __name__ == '__main__':
    args = get_option()
    current_frequency = args.current
    target_frequency = args.target
    file_path = args.tub
    if not args.test:
        main()
    else:
        test()
