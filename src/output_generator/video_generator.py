import cv2
import os
import subprocess, os, platform
import numpy as np
def gen_video(source,destination):
    image_folder = source
    video_name = destination

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    order = [int(i.split(".")[0][6:]) for i in images]
    sort = np.argsort(order)
    images = list(np.array(images)[sort])
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def call_video_generator(algorithm, output_file_name):
    input_dir =""
    if algorithm == "affinity clustering":
        input_dir = "Outputs/AffinityPropogations"
    elif algorithm == "kmeans":
        input_dir = "Outputs/Kmeans"
    elif algorithm == "dbscan":
        input_dir = "Outputs/DBScan"
    else:
        print("Invalid algorithm name")
    gen_video(input_dir, output_file_name)
    if platform.system() == 'Windows':
        os.startfile(output_file_name)
    else:                                   # linux variants
        subprocess.call(('xdg-open', output_file_name))

        