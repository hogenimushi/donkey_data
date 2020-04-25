import os
import json
import numpy as np
from argparse import ArgumentParser
import shutil


class ChangeFreqImg:
    def __init__(self, in_path, current_freq, target_freq, out_path):
        self.in_img_path = in_path + "/{}_cam-image_array_.jpg"
        self.data_num = []
        self.each_num = int(current_freq / target_freq)
        self.out_img_path = out_path + "_{}/{}_cam-image_array_.jpg"
        self.app_block = int(current_freq / 4)

    def remake_img(self):
        print("changing image frequency ...")
        for i in self.data_num:
            if (i % self.each_num) == 0:
                for j in range((i - self.each_num + 1), i + 1):
                    shutil.copyfile(self.in_img_path.format(j), self.out_img_path.format(((j-1) % self.each_num),
                                                                                         int((i+1)/self.each_num)))


class ChangeFreqJson:
    def __init__(self, in_path, current_freq, target_freq, out_path):
        self.in_json_path = in_path + "/record_{}.json"
        self.out_json_path = out_path + "_{}/record_{}.json"
        self.data_num = []
        self.angle = 0
        self.throttle = 0
        self.each_num = int(current_freq / target_freq)

    def remake_json(self):
        print("changing json frequency ...")
        for i in self.data_num:
            with open(self.in_json_path.format(i), 'r') as f:
                tmp = json.load(f)
                self.angle += float(tmp["user/angle"])
                self.throttle += float(tmp["user/throttle"])
            if (i % self.each_num) == 0:
                tmp["user/angle"] = self.angle/self.each_num
                tmp["user/throttle"] = self.throttle/self.each_num
                tmp["cam/image_array"] = "{}_cam-image_array_.jpg".format(int(i/self.each_num))
                for j in range((i-self.each_num+1), i+1):
                    with open(self.out_json_path.format(((j-1) % self.each_num), int((i+1) / self.each_num)), 'w') as g:
                        json.dump(tmp, g)
                self.angle = 0
                self.throttle = 0


class ApproximateChangeFreqJson:
    def __init__(self, in_path, current_freq, target_freq, out_path):
        self.in_json_path = in_path + "/record_{}.json"
        self.data_num = []
        self.angle = []
        self.throttle = []
        self.each_num = int(current_freq / target_freq)
        self.app_block = int(current_frequency/4)
        self.out_json_path = out_path + "_{}/record_{}.json"

    def remake_json(self):
        print("changing json frequency ...")
        for i in self.data_num:
            with open(self.in_json_path.format(i), 'r') as f:
                tmp = json.load(f)
                self.angle.append(float(tmp["user/angle"]))
                self.throttle.append(float(tmp["user/throttle"]))
        for i in self.data_num[self.app_block:(-1*self.app_block)]:
            res_angle = np.polyfit(self.data_num[i-self.app_block:i+self.app_block],
                                   self.angle[i-self.app_block:i+self.app_block], 3)
            res_throttle = np.polyfit(self.data_num[i-self.app_block:i+self.app_block],
                                      self.throttle[i-self.app_block:i+self.app_block], 3)
            with open(self.in_json_path.format(i), 'r') as f:
                tmp = json.load(f)
                tmp["user/angle"] = np.poly1d(res_angle)(self.data_num[i])
                tmp["user/throttle"] = np.poly1d(res_throttle)(self.data_num[i])
                tmp["cam/image_array"] = "{}_cam-image_array_.jpg".format(int((i-self.app_block)/self.each_num)+1)
            if (i % self.each_num) == 0:
                for j in range((i - self.each_num + 1), i + 1):
                    with open(self.out_json_path.format(((j-self.app_block-1) % self.each_num),
                                                        int((i-self.app_block+1)/self.each_num)), 'w') as f:
                        json.dump(tmp, f)


def verification_data(path):
    print("checking " + path + " ... ", end="")
    if os.path.exists(path + "/meta.json"):
        print("ok")
        return
    else:
        print("\n" + path + "doesn't exist donkey data.")
        exit(1)


def make_target_dir(path, current_freq, target_freq):
    print("making destination directory ...")
    for i in range(int(current_freq/target_freq)):
        os.mkdir(path + "_{}".format(i))
        print("making " + path + "_{}".format(i) + " ...")


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
    argparser.add_argument('--input', type=str, help="tab_path")
    argparser.add_argument('--test', action='store_true', help="if using test mode, --test option")
    argparser.add_argument('--output', type=str, help="destination_path")
    return argparser.parse_args()


def main():
    verification_data(input_path)
    make_target_dir(output_path, current_frequency, target_frequency)
    i = ChangeFreqImg(input_path, current_frequency, target_frequency, output_path)
    i.data_num = make_data_list(i.in_img_path)
    i.remake_img()
    j = ChangeFreqJson(input_path, current_frequency, target_frequency, output_path)
    j.data_num = i.data_num
    j.remake_json()
    print("finish changing frequency!")


def test():
    #verification_data(input_path)
    make_target_dir(output_path, current_frequency, target_frequency)
    i = ChangeFreqImg(input_path, current_frequency, target_frequency, output_path)
    i.data_num = make_data_list(i.in_img_path)
    j = ApproximateChangeFreqJson(input_path, current_frequency, target_frequency, output_path)
    j.data_num = i.data_num
    i.data_num = i.data_num[:-2*i.app_block+2]
    i.remake_img()
    j.remake_json()
    print("finish changing frequency!")


if __name__ == '__main__':
    args = get_option()
    current_frequency = args.current
    target_frequency = args.target
    input_path = args.input
    output_path = args.output
    if not args.test:
        main()
    else:
        test()
