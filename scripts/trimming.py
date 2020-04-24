import trimming_data
from argparse import ArgumentParser


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--num', nargs='+', type=int, help="input number directory")
    argparser.add_argument('--output', type=str, help="output data path")
    argparser.add_argument('--input', type=str, help="input data path")
    argparser.add_argument('--file', type=str, default="", help="if using input file, --file option")
    return argparser.parse_args()


def file_mode(file_dir, current_dir, target_dir):
    with open(file_dir) as f:
        line = [s.strip() for s in f.readlines()]
    num = [i.split() for i in line]
    for i in range(len(num)):
        trimming_data.main(current_dir, int(num[i][0]), int(num[i][1]), target_dir + '_{}'.format(i))


def arg_mode(num, current_dir, target_dir):
    for i in range(0, len(num), 2):
        trimming_data.main(current_dir, int(num[i]), int(num[i+1]), target_dir + '_{}'.format(i))


if __name__ == '__main__':
    args = get_option()
    current_path = args.input
    target_path = args.output
    file_path = args.file
    number_list = args.num
    if len(args.file) != 0:
        file_mode(file_path, current_path, target_path)
    else:
        arg_mode(number_list, current_path, target_path)
