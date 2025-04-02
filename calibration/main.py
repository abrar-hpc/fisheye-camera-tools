
import argparse
import glob
import cv2
import numpy as np
import calibration


def main() -> None:
    """
    Main function to perform camera calibration on a set of images.
    """
    
    parser = argparse.ArgumentParser(description='Perform camera calibration on a set of images.')
    parser.add_argument('dataset', help='Path to the dataset of images.')
    parser.add_argument('--show', action='store_true', help='Display the images with found corners.')
    parser.add_argument('-r', '--row', type=int, default=5, help='Number of row of the chessboard used for the calibration. It should be nb_row - 1.')
    parser.add_argument('-c', '--column', type=int, default=9, help='Number of column of the chessboard used for the calibration. It should be nb_col - 1.')
    args = parser.parse_args()

    if not args.dataset.endswith('/'):
        print("Error : The provided dataset must be a valid directory and his path must end with '/'.")
        return
    files = args.dataset + '*'
    images: list[str] = glob.glob(files)

    # Defining the dimensions of the checkerboard
    checkerboard = args.row, args.column

    # Termination criteria for the iterative algorithm used to refine the corner positions
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objpoints, imgpoints, img_shape = calibration.find_corners(images, checkerboard, criteria, args.show)

    mtx, dist, rvecs, tvecs = calibration.calibrate_camera(objpoints, imgpoints, img_shape)


    print("\n Dimensions:")
    print(img_shape)

    print("\n Camera matrix:") 
    print(mtx) 
    
    print("\n Distortion coefficient:") 
    print(dist) 
    
    print("\n Rotation Vectors:") 
    print(rvecs) 
    
    print("\n Translation Vectors:") 
    print(tvecs) 
    np.savez(f"{args.dataset[:-1]}", mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    # To use these data :
    
    # data = np.load("path_of_data.npz")

    # mtx = data['mtx']
    # dist = data['dist']
    # rvecs = data['rvecs']
    # tvecs = data['tvecs']



    
if __name__ == '__main__':
    main()