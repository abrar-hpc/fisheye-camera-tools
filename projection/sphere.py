# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    sphere.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abrar <abrar.patel@ensiie.eu>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/16 16:42:02 by abrar             #+#    #+#              #
#    Updated: 2024/08/06 19:12:49 by abrar            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def project_on_sphere(img1: str, img2: str, show_axes: bool) -> None:
    """
    Projects the given images onto a sphere.

    Args:
        img1 (str): Path to the first image.
        img2 (str): Path to the second image.
        show_axes (bool): Whether to show the axes of the sphere.
    """
    # Load the images 
    # left_image = cv2.imread('back0.jpg')
    # right_image = Image.open('front0.jpg')


    with Image.open(img1) as left_image, Image.open(img2) as right_image:

        # Sphere parameters
        r = 1
        theta, phi = np.mgrid[0.0:np.pi:180j, 0.0:2.0*np.pi:360j]
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        
        # Resize the images to match the dimensions of the spherical grid
        left_image = left_image.resize((theta.shape[0], phi.shape[1] // 2))
        right_image = right_image.resize((theta.shape[0], phi.shape[1] // 2))

        # Convert the resized images to numpy arrays
        left_image = np.array(left_image) / 255.0  # Normalize color values between 0 and 1
        right_image = np.array(right_image) / 255.0

        # Display the recentered images
        fig, axes = plt.subplots(1, 2, figsize=(15, 7))
        axes[0].imshow(left_image)
        axes[0].set_title("Recentered Left Image")
        axes[0].axis('off')

        axes[1].imshow(right_image)
        axes[1].set_title("Recentered Right Image")
        axes[1].axis('off')

        plt.show()

        # Create an array for the sphere's surface colors
        facecolors = np.empty(x.shape + (3,), dtype=np.float64)

        # Apply the images to the hemispheres
        for i in range(facecolors.shape[0]):
            for j in range(facecolors.shape[1]):
                if y[i, j] >= 0:
                    # Right hemisphere
                    facecolors[i, j] = right_image[i, j % (theta.shape[1] // 2)]
                else:
                    # Left hemisphere
                    facecolors[i, j] = left_image[i, j % (theta.shape[1] // 2)]

        # Create the figure and axes
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Project the images onto the hemispheres
        ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=facecolors, antialiased=True, shade=False)

        # Hide the axes
        if not show_axes:
            ax.set_axis_off()

        # Adjust the axes
        ax.set_box_aspect([1,1,1])

        # Display the sphere
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description='Project fisheye images on a sphere.')
    parser.add_argument('image1', help='Path to the fisheye image on the left.')
    parser.add_argument('image2', help='Path to the fisheye image on the right.')
    parser.add_argument('--show-axes', action='store_true', help='Show the axes on the plot.')
    args = parser.parse_args()

    print('Running...')
    project_on_sphere(args.image1, args.image2, args.show_axes)
    print('Done.')


if __name__ == '__main__':
    main()
