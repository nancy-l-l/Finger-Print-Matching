import os, cv2, glob, math, numpy as np
import matplotlib.pyplot as plt
#from scipy.ndimage import gaussian_filter
#import matplotlib.image as mpimg
import clean
import ridge_orientation
#import imageio.v3 as iio
#from PIL import Image   
#from scipy.spatial import cKDTree
#from skimage.morphology import (
#    skeletonize, remove_small_objects, disk, closing, dilation
#)
from scipy.ndimage import rotate
#from crossing_number import calculate_minutiae, draw_minutiae
from poincare import find_singularities, draw_singularities
from create_graphs import create_graph
#from augment import rotate
import random
import graph
import fingerprint_feature_extractor
import upload
def plot_tuples(data):
    """
    Sort a list of (x, y) tuples by x and plot them.

    Parameters
    ----------
    data : list[tuple[float, float]]
        Each tuple is (x, y).  The first element is plotted on the X-axis,
        the second on the Y-axis.
    """
    # 1️⃣ Sort by the first element (x value)
    data = sorted(data, key=lambda t: t[0])

    # 2️⃣ Split into X and Y
    xs, ys = zip(*data)

    # 3️⃣ Make the graph
    plt.figure(figsize=(6, 4))
    plt.plot(xs, ys, marker='o')           # default colour & style
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Tuples plotted after sorting by X")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    ROOT_DIR  = "fingerprints"
    SUBDIRS   = ["DB1_B", "DB2_B", "DB3_B", "DB4_B"]
    graphs = []
    rotated_graphs = []
    similarity_score = {}
    test_similarity_score = {}
    count = 0
    correct=0
    n=30
    angle_scores = []
    for db in SUBDIRS:
        dir_path = os.path.join(ROOT_DIR, db)
        if not os.path.isdir(dir_path):
            print(f"⚠️  {dir_path} not found – skipping")
            continue

        for root, _, files in os.walk(dir_path):
            for fname in files:
                _, ext = os.path.splitext(fname)
            
                file_path = os.path.join(root, fname)
                
                g, rot_g, angle = upload.upload(file_path)
                
                #similarity_score is a dictionary with key as file_path
                #value is angle of rotated print. and similarity probability of print and corresponding rotated print
                similarity_probability, match = graph.wl_graph_similarity(rot_g, g, 1)
                similarity_score[file_path]=(angle, similarity_probability)
                test_similarity_score[file_path]=[]
                
                graphs.append((file_path, g))
                rotated_graphs.append((file_path, rot_g))
                
        
    #iterates over all combinations of graphs and rotated graphs, and adds their similarity probability to test_similarity_score
    #test_similarity_score is a dictionary with key as file_path
    #value is a list of tuples. each tuple has the comparing file_path and similarity prob
    for i in range(len(graphs)):
        for j in range(len(rotated_graphs)):
            name,g=graphs[i]
            rot_name,rot_g=rotated_graphs[j]
            similarity_probability_1, match_1 = graph.wl_graph_similarity(rot_g, g, 1)
            test_similarity_score[name].append((rot_name, similarity_probability_1))
            
    #iterates over every file and counts how many pairs score higher than the true matched pair (print and corresponding rotated print)
    for key, val in test_similarity_score.items():
        count = 0
        angle, same_score = similarity_score[key]
        print(key+": "+str(angle))
        print('-----------------------------------------')
        differences = []
        for score_tuple in val:
            rot_name, diff_score = score_tuple
            if same_score > diff_score:
                count+=1
        angle_scores.append(count/len(val))
        print("Accuracy: \t"+str(count/len(val)))
        print(" ")
    print(" ")
    print(" ")
    print("total accyracy")
    print('==========================================')
    print("Accuracy: "+str(sum(angle_scores)/len(angle_scores)))
    
