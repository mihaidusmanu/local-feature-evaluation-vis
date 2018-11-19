# Visualisation tools for LFE Benchmark

More information about this benchmark can be found in the following paper:

    "Comparative Evaluation of Hand-Crafted and Learned Local Features".
    J.L. Schönberger, H. Hardmeier, T. Sattler and M. Pollefeys. CVPR 2017.

[Paper](https://demuc.de/papers/schoenberger2017comparative.pdf),
[Supplementary](https://demuc.de/papers/schoenberger2017comparative_supp.pdf),
[Bibtex](https://demuc.de/papers/schoenberger2017comparative.bib),
[Repository](https://github.com/ahojnnes/local-feature-evaluation)

## Compare models

    python compare_registered_images.py --dataset_path /path/to/dataset --methods "method1 method2 ..."

This script compares different methods in terms of registered images. 
It can be useful to make sure that there are no wrong registrations due to repeated structures or similar scenes. 
The sparse models should be placed at `/path/to/dataset/sparse-method*/`.

## Isolate images

    dataset_path=/path/to/dataset
    python isolate_images.py --dataset_path $dataset_path --input_path $dataset_path/sparse/0 --output_path $dataset_path/sparse/0/submodel --im_list_path list.txt

This script isolates specific images from a large reconstruction. 
One possible use-case is to make sure that an image is correctly registered. 
Please note that COLMAP might throw an error for certain images _work in progress_.
