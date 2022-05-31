import numpy as np
import os
import matplotlib.pyplot as plt
from cv2 import cv2
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from imageio import imread
from skimage.transform import resize
from scipy.spatial import distance
import tensorflow as tf
from utils import face_detect
from utils import image_preprocess

def generate_image_encoding(path):
    
    image_dir_basepath = path

    model_path = 'static/model/keras/model/facenet_keras.h5'
    model = tf.python.keras.models.load_model(model_path, compile=False)

    image_dirpath = image_dir_basepath
    image_filepaths = [os.path.join(image_dirpath, f) for f in os.listdir(image_dirpath)]
    image_filepaths.append(image_filepaths[0])
    
    embs = image_preprocess.calc_embs(image_filepaths,model)
    return embs[0]