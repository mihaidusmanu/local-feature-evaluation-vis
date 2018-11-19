import argparse

import matplotlib.pyplot as plt

import os

from scipy.misc import imread

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", required = True,
                        help = "Path to the dataset, e.g. path/to/Fountain")
    parser.add_argument("--methods", required = True,
                        help = "Methods, e.g. \"sift lift\"")
    args = parser.parse_args()
    return args

def get_largest_sparse_model(sparse_path):
    models = os.listdir(sparse_path)
    if len(models) == 0:
        print("Warning: Could not reconstruct any model")
        return

    largest_model = None
    largest_model_num_images = 0
    for model in models:
        with open(os.path.join(sparse_path, model, "cameras.txt"), "r") as fid:
            for line in fid:
                if line.startswith("# Number of cameras"):
                    num_images = int(line.split()[-1])
                    if num_images > largest_model_num_images:
                        largest_model = model
                        largest_model_num_images = num_images
                    break

    return int(largest_model), largest_model_num_images

def get_images(model_path):
    images = []
    with open(os.path.join(model_path, "images.txt"), "r") as fid:
        for line in fid:
            line = line.strip("\n")
            if line.startswith("#"):
                continue
            if line.endswith(".jpg"):
                images.append(line.split()[-1])

    return images

def main():
    args = parse_args()

    print("Press <n> for next image")
    print("Press <p> for previous image")
    print("Press <r> to print the current image name")

    methods = args.methods.split()
    n_methods = len(methods)
    largest_model = [None] * n_methods
    largest_model_num_images = [None] * n_methods
    images = [None] * n_methods
    for idx, method in enumerate(methods):
        largest_model[idx], largest_model_num_images[idx] = get_largest_sparse_model(os.path.join(args.dataset_path, "sparse-" + method))
        print('[{:s}] Largest model {:02d} with {:04d} registered images.'.format(method, largest_model[idx], largest_model_num_images[idx]))
        
        images[idx] = get_images(os.path.join(args.dataset_path, "sparse-" + method, str(largest_model[idx])))

    for idx in range(n_methods):
        for idx_ in range(n_methods):
            if idx == idx_:
                continue
            diff = sorted(list(set(images[idx]) - set(images[idx_])))
            print("[{:s} - {:s}] {:04d} images".format(methods[idx], methods[idx_], len(diff)))
            
            def redraw(fig, f, event = None):
                action = 'n'
                if event is not None:
                    action = event.key
                if action in ['N', 'n']:
                    redraw.img_idx = (redraw.img_idx + 1) % len(diff)
                    
                    fig.clear()
                    
                    img_idx = redraw.img_idx
                    img_name = diff[img_idx]
                    img = imread(os.path.join(args.dataset_path, "images", img_name))
                    
                    ax = fig.add_subplot(1, 1, 1)
                    ax.imshow(img)
                    ax.axis("off")
                    ax.set_title("{:04d} / {:04d} - {:s}".format(img_idx + 1, len(diff), img_name))
                    
                    plt.draw()
                elif action in ['P', 'p']:
                    redraw.img_idx = (redraw.img_idx - 1 + len(diff)) % len(diff)

                    fig.clear()
                    
                    img_idx = redraw.img_idx
                    img_name = diff[img_idx]
                    img = imread(os.path.join(args.dataset_path, "images", img_name))
                    
                    ax = fig.add_subplot(1, 1, 1)
                    ax.imshow(img)
                    ax.axis("off")
                    ax.set_title("{:04d} / {:04d} - {:s}".format(img_idx + 1, len(diff), img_name))
                    
                    plt.draw()
                elif action in ['R', 'r']:
                    img_idx = redraw.img_idx
                    img_name = diff[img_idx]
                    print("{:s}".format(img_name))
                    f.write("{:s}\n".format(img_name))
            redraw.img_idx = -1
            
            fig = plt.figure()
            f = open("{:s}-{:s}.txt".format(methods[idx], methods[idx_]), "w")
            redraw(fig, f)
            fig.canvas.mpl_connect('key_press_event', lambda event: redraw(fig, f, event))
            plt.show()
            f.close()

if __name__ == "__main__":
    main()
