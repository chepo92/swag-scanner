#!/usr/opt/python3

from __future__ import print_function

import numpy as np
from numpy import cos, sin
from numpy.testing import assert_equal
import unittest
import swagscanner.visualization.viewer as viewer

import pcl
# from pcl.pcl_registration import icp, gicp, icp_nl
from pcl import IterativeClosestPoint, GeneralizedIterativeClosestPoint, IterativeClosestPointNonLinear


class TestICP(unittest.TestCase):
    def setUp(self):
        # Check if ICP can find a mild rotation.
        theta = [-.031, .4, .59]
        rot_x = [[1, 0, 0],
                 [0, cos(theta[0]), -sin(theta[0])],
                 [0, sin(theta[0]), cos(theta[0])]]
        
        rot_y = [[cos(theta[1]), 0, sin(theta[1])],
                 [0, 1, 0],
                 [-sin(theta[1]), 0, cos(theta[1])]]
        
        rot_z = [[cos(theta[2]), -sin(theta[1]), 0],
                 [sin(theta[2]), cos(theta[1]), 0],
                 [0, 0, 1]]
        # print(rot_x)
        # print(rot_y)
        # print(rot_z)
        transform = np.dot(rot_x, np.dot(rot_y, rot_z))
        # print(transform)

        source = np.random.RandomState(42).randn(900, 3)
        self.source = pcl.PointCloud(source.astype(np.float32))

        target = np.dot(source, transform)
        self.target = pcl.PointCloud(target.astype(np.float32))
        print(self.target)

        # self.source = pcl.load('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/0.pcd')
        # print(self.source.size)
        # sor = self.source.make_voxel_grid_filter()
        # sor.set_leaf_size(0.01, 0.01, 0.01)
        # self.source = sor.filter()
        # print(self.source.size)

        # self.target = pcl.load('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/18.pcd')
        # sor2 = self.target.make_voxel_grid_filter()
        # sor2.set_leaf_size(0.01, 0.01, 0.01)
        # self.target = sor2.filter()
        # print(self.target.size)
        # print(dir(self.source.make_IterativeClosestPoint()))

    def testICP(self):
        icp = self.source.make_IterativeClosestPoint()
        print(dir(icp))
        converged, transf, estimate, fitness = icp.icp(
            self.source, self.target, max_iter=1000)

        self.assertTrue(converged is True)
        
        
        print('has converged:' + str(converged) + ' score: ' + str(fitness))
        print(str(transf))
        print(estimate)

        self.assertTrue(isinstance(transf, np.ndarray))
        self.assertEqual(transf.shape, (4, 4))

        self.assertFalse(np.any(transf[:3] == 0))
        assert_equal(transf[3], [0, 0, 0, 1])

        viewer.visualize(estimate)

        # XXX I think I misunderstand fitness, it's not equal to the following MSS.
        # mss = (np.linalg.norm(estimate.to_array()
        #                       - self.source.to_array(), axis=1) ** 2).mean()
        # self.assertLess(mss, 1)

        # print("------", algo)
        # print("Converged: ", converged, "Estimate: ", estimate,
        #       "Fitness: ", fitness)
        # print("Rotation: ")
        # print(transf[0:3,0:3])
        # print("Translation: ", transf[3, 0:3])
        # print("---------")


class TestGICP(unittest.TestCase):
    def setUp(self):
        # Check if ICP can find a mild rotation.
        theta = [-.031, .4, .59]
        rot_x = [[1, 0, 0],
                 [0, cos(theta[0]), -sin(theta[0])],
                 [0, sin(theta[0]), cos(theta[0])]]
        rot_y = [[cos(theta[1]), 0, sin(theta[1])],
                 [0, 1, 0],
                 [-sin(theta[1]), 0, cos(theta[1])]]
        rot_z = [[cos(theta[2]), -sin(theta[1]), 0],
                 [sin(theta[2]), cos(theta[1]), 0],
                 [0, 0, 1]]
        transform = np.dot(rot_x, np.dot(rot_y, rot_z))

        source = np.random.RandomState(42).randn(900, 3)
        self.source = pcl.PointCloud(source.astype(np.float32))

        target = np.dot(source, transform)
        self.target = pcl.PointCloud(target.astype(np.float32))

    def testGICP(self):
        gicp = self.source.make_GeneralizedIterativeClosestPoint()
        converged, transf, estimate, fitness = gicp.gicp(
            self.source, self.target, max_iter=1000)

        self.assertTrue(converged is True)
        self.assertLess(fitness, .1)

        self.assertTrue(isinstance(transf, np.ndarray))
        self.assertEqual(transf.shape, (4, 4))

        self.assertFalse(np.any(transf[:3] == 0))
        assert_equal(transf[3], [0, 0, 0, 1])

        # XXX I think I misunderstand fitness, it's not equal to the following
        # MSS.
        # mss = (np.linalg.norm(estimate.to_array()
        #                       - self.source.to_array(), axis=1) ** 2).mean()
        # self.assertLess(mss, 1)

        # print("------", algo)
        # print("Converged: ", converged, "Estimate: ", estimate, "Fitness: ", fitness)
        # print("Rotation: ")
        # print(transf[0:3,0:3])
        # print("Translation: ", transf[3, 0:3])
        # print("---------")


class TestICP_NL(unittest.TestCase):
    def setUp(self):
        # Check if ICP can find a mild rotation.
        theta = [-.031, .4, .59]
        rot_x = [[1, 0, 0],
                 [0, cos(theta[0]), -sin(theta[0])],
                 [0, sin(theta[0]), cos(theta[0])]]
        rot_y = [[cos(theta[1]), 0, sin(theta[1])],
                 [0, 1, 0],
                 [-sin(theta[1]), 0, cos(theta[1])]]
        rot_z = [[cos(theta[2]), -sin(theta[1]), 0],
                 [sin(theta[2]), cos(theta[1]), 0],
                 [0, 0, 1]]
        transform = np.dot(rot_x, np.dot(rot_y, rot_z))

        source = np.random.RandomState(42).randn(900, 3)
        self.source = pcl.PointCloud(source.astype(np.float32))

        target = np.dot(source, transform)
        self.target = pcl.PointCloud(target.astype(np.float32))
        


    def testICP_NL(self):
        icp_nl = self.source.make_IterativeClosestPointNonLinear()
        converged, transf, estimate, fitness = icp_nl.icp_nl(
            self.source, self.target, max_iter=1000)

        self.assertTrue(converged is True)
        # fail: pcl 1.9.1 
        # self.assertLess(fitness, .1)

        self.assertTrue(isinstance(transf, np.ndarray))
        self.assertEqual(transf.shape, (4, 4))

        self.assertFalse(np.any(transf[:3] == 0))
        assert_equal(transf[3], [0, 0, 0, 1])

        # XXX I think I misunderstand fitness, it's not equal to the following
        # MSS.
        # mss = (np.linalg.norm(estimate.to_array()
        #                       - self.source.to_array(), axis=1) ** 2).mean()
        # self.assertLess(mss, 1)
        # print("------", algo)
        # print("Converged: ", converged, "Estimate: ", estimate,
        #       "Fitness: ", fitness)
        # print("Rotation: ")
        # print(transf[0:3,0:3])
        # print("Translation: ", transf[3, 0:3])
        # print("---------")


_data = [(i, 2 * i, 3 * i + 0.2) for i in range(5)]
_DATA = """0.0, 0.0, 0.2;
           1.0, 2.0, 3.2;
           2.0, 4.0, 6.2;
           3.0, 6.0, 9.2;
           4.0, 8.0, 12.2"""

# registration
### GeneralizedIterativeClosestPoint ###


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestICP))

    return suite


if __name__ == '__main__':
    testSuite = suite()
    unittest.TextTestRunner().run(testSuite)
