# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    calibration.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abrar <abrar.patel@ensiie.eu>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/27 15:57:02 by abrar             #+#    #+#              #
#    Updated: 2024/09/10 11:40:49 by abrar            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cv2
import numpy as np
from typing import Tuple

def find_corners(images: list[str], checkerboard: Tuple[int, int], criteria: Tuple[int, int, float], show: bool = False) -> Tuple[list[np.ndarray], list[np.ndarray], Tuple[int, int]]:
    """
    Finds the corners in the provided images for camera calibration.

    Args:
    images: List of paths to the images containing the checkerboard pattern.
    checkerboard: Number of internal corners per a chessboard row and column.
    criteria: Criteria for the cornerSubPix algorithm.

    Returns:
    objpoints: List of 3D points in real-world space for each checkerboard image.
    imgpoints: List of 2D points in image plane for each checkerboard image.
    img_shape: Shape of the grayscale image used for calibration.
    show: Whether to display the images with found corners.
    """
    # List to store 3D and 2D points for each image
    objpoints: list[np.ndarray] = []
    imgpoints: list[np.ndarray] = []

    # Prepare a single set of 3D points for the checkerboard pattern
    objp = np.zeros((1, checkerboard[0] * checkerboard[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:checkerboard[0], 0:checkerboard[1]].T.reshape(-1, 2)
    
    # Iterate through each image to find chessboard corners
    for fname in images:
        #print(f"{fname = }")
        img = cv2.imread(fname)  
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners in the image
        ret, corners = cv2.findChessboardCorners(gray, checkerboard,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + 
                                                 cv2.CALIB_CB_FAST_CHECK + 
                                                 cv2.CALIB_CB_NORMALIZE_IMAGE)

        # If corners are found, refine the corner positions and store the points
        
        if ret:
            print(fname)
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Optionally, draw and display the corners
            if show:
                img = cv2.drawChessboardCorners(img, checkerboard, corners2, ret)
                cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                cv2.imshow('img', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        else:
            #print(f"{fname}")
            ()


    return objpoints, imgpoints, gray.shape[::-1]

def calibrate_camera(objpoints: list[np.ndarray], imgpoints: list[np.ndarray], img_shape: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray, list[np.ndarray], list[np.ndarray]]:
    """
    Performs camera calibration given object points and image points.

    Args:
    objpoints: List of 3D points in real-world space for each checkerboard image.
    imgpoints: List of 2D points in image plane for each checkerboard image.
    img_shape: Shape of the grayscale image used for calibration.

    Returns:
    mtx: Camera matrix.
    dist: Distortion coefficients.
    rvecs: List of rotation vectors estimated for each pattern view.
    tvecs: List of translation vectors estimated for each pattern view.
    """
    _, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_shape, None, None)
    print(len(rvecs))
    return mtx, dist, rvecs, tvecs

if __name__ == '__main__':
    ()