import argparse

import matplotlib.pyplot as plt

import os

from scipy.misc import imread

import shutil

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", required = True,
                        help = "Path to the dataset, e.g. path/to/Fountain")
    parser.add_argument("--input_path", required = True)
    parser.add_argument("--output_path", required = True)
    parser.add_argument("--im_list_path", required = True)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    
    if not os.path.isdir(args.output_path):
        os.mkdir(args.output_path)

    shutil.copy2(os.path.join(args.input_path, "project.ini"), os.path.join(args.output_path, "project.ini"))
    shutil.copy2(os.path.join(args.input_path, "cameras.txt"), os.path.join(args.output_path, "cameras.txt"))
    shutil.copy2(os.path.join(args.input_path, "points3D.txt"), os.path.join(args.output_path, "points3D.txt"))
    shutil.copy2(os.path.join(args.input_path, "images.txt"), os.path.join(args.output_path, "images_all.txt"))

    with open(args.im_list_path, "r") as f:
        im_names = f.readlines()
        im_names = [im_name.strip() for im_name in im_names]

    with open(os.path.join(args.output_path, "images_all.txt"), "r") as f:
        lines = f.readlines()
        
    with open(os.path.join(args.output_path, "images.txt"), "w") as f:
        start_line_idx = 0
        while lines[start_line_idx][0] == '#':
            start_line_idx += 1
        for line_idx in range(start_line_idx, len(lines), 2):
            if lines[line_idx].split()[-1] in im_names:
                f.write(lines[line_idx])
                f.write(lines[line_idx + 1])

if __name__ == "__main__":
    main()
