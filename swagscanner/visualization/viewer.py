'''Visualization tools

'''

import os
import pcl
import pcl.pcl_visualization
import random
import re
import time
from swagscanner.utils.file import FileSaver

import numpy as np


def visualize(source, target=None, registered=None):
    '''Visualize a pointcloud. Can handle multiple cloud inputs.
    The base cloud will be colored blue, the rest are randomly colored.

    Args:
        cloud (PointCloudXYZ): the pointcloud you want to visualize

    '''

    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
        source, 255, 255, 0)
    viewer.AddPointCloud_ColorHandler(source, pccolor, bytes(1), 0)

    if target:
        pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
            target, 0, 0, 255)
        viewer.AddPointCloud_ColorHandler(target, pccolor, bytes(2), 0)

    if registered:
        pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
            registered, 0, 255, 0)
        viewer.AddPointCloud_ColorHandler(registered, pccolor, bytes(3), 0)

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)


def visualize_from_file(path, *paths):
    '''Visualize a pointcloud given file path. Can handle multiple file inputs

    Args:
        path (str): path to the pointcloud you want to visualize

    '''

    point_cloud = pcl.load(path)
    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    viewer.AddPointCloud(point_cloud, b'scene_cloud', 0)
    count = 0
    for path in paths:
        cloud = pcl.load(path)
        viewer.AddPointCloud(cloud, b'%b' % bytes(count), 0)
        count += 1

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)


def visualize_from_folder(folder_path):
    '''Visualize all the pointclouds in a given folder

    '''

    file_saver = FileSaver(folder_path=folder_path)
    cloud_list = file_saver.get_cloud_list(folder_path)

    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    count = 0

    for cloud in cloud_list:
        cloud = pcl.load(cloud)
        viewer.AddPointCloud(cloud, b'%b' % bytes(count), 0)
        count += 1

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)


def main():
    visualize_from_folder(
        '/Users/seanngpack/Programming Stuff/Projects/scanner_files/15/registration')
    # visualize_from_file('/Users/seanngpack/Programming Stuff/Projects/scanner_files/14/registration/0.pcd',
    #                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/14/registration/1.pcd',
    #                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/14/registration/2.pcd',
    #                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/14/registration/3.pcd',
    #                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/14/registration/4.pcd',
    #                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/14/registration/5.pcd',                        
    #                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/14/registration/6.pcd',
    #                     )
    # visualize_from_file('/Users/seanngpack/Programming Stuff/Projects/scanner_files/12/registration/0.pcd',
    #                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/12/registration/1.pcd')
    # visualize_from_file('/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/0.pcd')


if __name__ == "__main__":
    main()
