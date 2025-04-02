# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    image_processor.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abrar <abrar.patel@ensiie.eu>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/27 15:58:39 by abrar             #+#    #+#              #
#    Updated: 2024/07/22 20:54:16 by abrar            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


"""
Script to read and split images using OpenCV

This script demonstrates how to read images, split them into left and right halves, 
display the processed images.
"""

import os
import cv2 
from typing import Tuple


def split_image(img: cv2.Mat) -> Tuple[cv2.Mat, cv2.Mat]:
    """
    Split an image into left and right halves.

    Parameters
    ----------
    img : The image matrix to be split.

    Returns
    -------
    The left and right halves of the image.
    """
    _, w, _ = img.shape  # (height, width, number_of_channels)
    half = w // 2  # Calculate the midpoint of the width
    left_part = img[:, :half]  # Extract the left half
    right_part = img[:, half:]  # Extract the right half
    return left_part, right_part


def video_to_frames(video_path: str, output_dir: str):
    """
    Decompose a video into frames and save them as images.

    Parameters
    ----------
    video_path: str, path to the input video file.
    output_dir: str, directory to save the frames.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the video
    cap = cv2.VideoCapture(video_path)

    # Check if the video is opened successfully
    if not cap.isOpened():
        print("Error: Could not open the video.")
        return

    frame_number = 0

    while True:
        # Read a frame
        ret, frame = cap.read()

        # If reading fails, exit the loop
        if not ret:
            break

        # Define the output file name
        frame_filename = os.path.join(output_dir, f'frame_{frame_number:04d}.jpg')

        # Save the frame as an image
        cv2.imwrite(frame_filename, frame)

        frame_number += 1

    # Release the resources
    cap.release()

    print(f'Total frames: {frame_number}')
    print('Video decomposition completed.')





def main(img_name: str) -> None:
    img = cv2.imread(img_name)
    r,l = split_image(img)
    cv2.imshow(f"{img_name}_r", r)
    cv2.imshow(f"{img_name}_l", l)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        return


if __name__ == "__main__":
    # Example usage
    # image_name = 
    # main(image_name)
    video_path = 'acquisition/time/video_front.mp4'
    output_dir = 'acquisition/time/frames_front'
    video_to_frames(video_path, output_dir)
    ()