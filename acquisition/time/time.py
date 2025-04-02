# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    time.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abrar <abrar.patel@ensiie.eu>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/12 16:54:13 by abrar             #+#    #+#              #
#    Updated: 2024/08/06 18:04:21 by abrar            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt

def calculate_mean_and_std(data: np.ndarray) -> Tuple[float, float]:
    """
    Calculate the mean and standard deviation of a sample of data.

    Parameters:
    - data: numpy array of numerical values

    Returns:
    - mean: float, the mean of the data
    - std_dev: float, the standard deviation of the data
    """
    mean = np.mean(data)
    std_dev = np.std(data)
    return mean, std_dev

def plot_data_with_statistics(data: np.ndarray, mean: float, std_dev: float, lens: str, axs: np.ndarray) -> None:
    """
    Plot the data along with its mean and standard deviation.

    Parameters:
    - data: numpy array of numerical values
    - mean: float, the mean of the data
    - std_dev: float, the standard deviation of the data
    - lens: str, the type of lens (e.g., 'back', 'front')
    - axs: numpy array of matplotlib axes objects for the subplots
    """
    i = 0 if lens == 'back' else 1

    # Histogram of the data
    axs[i].hist(data, bins=10, alpha=0.7, color='g', edgecolor='black', label='Data')

    # Line for the mean
    axs[i].axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Mean: {mean:f}')

    # Areas for standard deviation
    axs[i].axvline(mean - std_dev, color='b', linestyle='dotted', linewidth=2, label=f'-1 Std Dev: {mean - std_dev:f}')
    axs[i].axvline(mean + std_dev, color='b', linestyle='dotted', linewidth=2, label=f'+1 Std Dev: {mean + std_dev:f}')
    axs[i].text(0.45, 9, f"Std Dev: {std_dev:f}")
    # Title and labels
    axs[i].set_title(f'Data Distribution with Mean and Standard Deviation of the {lens} lens')
    axs[i].set_xlabel('Acquisition time (seconds)')
    axs[i].set_ylabel('Frequency')
    axs[i].legend()

    all_data_y = np.append(data, [mean, mean + std_dev, mean - std_dev])
    y_max = max(all_data_y) + 12
    axs[i].set_ylim(0, y_max)
    axs[i].set_xlim(0.3, 0.52)



def compute(data: np.ndarray, lens: str, axs: np.ndarray) -> None:
    """
    Compute and print the mean and standard deviation of the data for a given lens.

    Parameters:
    - data: numpy array of numerical values
    - lens: str, the type of lens (e.g., 'back', 'front')
    - axs: numpy array of matplotlib axes objects for the subplots
    """

    # Calculate mean and standard deviation
    mean, std_dev = calculate_mean_and_std(data)

    print(f'{lens[0].upper()}{lens[1:].lower()}:')
    # Print the mean and standard deviation
    print(f'Mean: {mean:f}')
    print(f'Standard Deviation: {std_dev:f}\n')

    # Plot the data with mean and standard deviation
    plot_data_with_statistics(data, mean, std_dev, lens, axs)


def main() -> None:
    real_back: list[float]        = [26.07, 26.10, 26.14, 26.17, 26.17, 26.21, 26.24, 26.28, 26.31, 26.35, 26.35,
                                     26.38, 26.41, 26.45, 26.52, 26.55, 26.65, 26.72, 26.82, 26.86, 26.89, 26.93,
                                     26.96, 27.00, 27.03, 27.06, 27.10, 27.13, 27.17, 27.20, 27.23, 27.30, 27.34,
                                     27.95, 27.95, 28.02, 28.05, 28.05, 28.12, 28.15, 28.19, 28.29, 28.33, 28.35] 

    acquisition_back: list[float] = [25.62, 25.73, 25.73, 25.73, 25.83, 25.83, 25.83, 25.93, 25.93, 25.93, 26.03,
                                     26.03, 26.03, 26.03, 26.14, 26.14, 26.21, 26.21, 26.41, 26.52, 26.52, 26.52,
                                     26.62, 26.62, 26.62, 26.72, 26.72, 26.72, 26.72, 26.82, 26.82, 26.93, 26.93,
                                     27.51, 27.61, 27.61, 27.61, 27.72, 27.72, 27.82, 27.82, 27.92, 27.92, 28.02] 

    delta_back = [real_back[i] - acquisition_back[i] for i in range(len(real_back))]
    data_back = np.array(delta_back)


    real_front: list[float]        = [37.93, 37.96, 38.00, 38.03, 38.07, 38.10, 38.41, 38.44, 38.44, 38.51, 38.55,
                                      38.58, 38.61, 38.65, 38.68, 38.72, 38.75, 38.78, 38.82, 38.85, 38.89, 38.92, 
                                      38.95, 38.99, 39.02, 39.06, 39.09, 39.12, 39.16, 39.19, 40.42, 40.45, 40.49, 
                                      40.52, 40.56, 40.59, 40.63, 40.66, 40.69, 40.73, 40.80, 40.83, 40.86, 40.90] 

    acquisition_front: list[float] = [37.55, 37.55, 37.69, 37.69, 37.69, 37.75, 38.07, 38.07, 38.07, 38.17, 38.17, 
                                      38.27, 38.27, 38.27, 38.27, 38.37, 38.37, 38.37, 38.37, 38.37, 38.48, 38.48, 
                                      38.48, 38.68, 38.68, 38.68, 38.68, 38.79, 38.79, 38.79, 40.08, 40.08, 40.18, 
                                      40.18, 40.18, 40.28, 40.28, 40.28, 40.28, 40.39, 40.39, 40.45, 40.45, 40.45]

    delta_front = [real_front[i] - acquisition_front[i] for i in range(len(real_front))]
    data_front = np.array(delta_front)

    _, axs = plt.subplots(1, 2, figsize=(14, 6))

    compute(data_back, 'back', axs)
    compute(data_front, 'front', axs)
    
    # Adjust layout
    plt.tight_layout()
    plt.savefig(f'acquisition/time/acquisition_time.jpg')
    plt.show()



if __name__ == '__main__':
    main()