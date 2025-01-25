import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file
import time
import numpy as np
import sys
import time
import numpy as np
from typing import List, Tuple
from itertools import combinations
from a1_utils import (
    distance,
    generate_random_input_file,
    read_input_from_cli,
    write_output_to_file,
    sort_pairs
)

def divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Recursively find the closest pair of points using a divide-and-conquer approach.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points where 
                                            each point is represented as a tuple (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The minimum distance between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """
    n = len(points)
    # Solve if <= 3 points
    if n <= 3:
        pairs = []
        min_dist = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                d = distance(points[i], points[j])
                if d < min_dist:
                    min_dist = d
                    pairs = [(points[i], points[j])]
                elif d == min_dist:
                    pairs.append((points[i], points[j]))
        
        return min_dist, pairs
    
    # If there's more than 3 points
    # we will enter the recursive section

    # sort first by x
    points_x = sorted(points, key=lambda x: x[0])

    # calculate left and right
    median_n = math.floor(n / 2)
    
    # calculate median_x
    median_x = points_x[median_n][0]
    if n % 2 == 0:
        median_x = (points_x[median_n - 1][0] + median_x) / 2
    
    left = []
    right = []
    
    for point in points:
        if point[0] <= median_x:
            left.append(point)
        else:
            right.append(point)

    d1, p1 = divide_and_conquer_closest_pair(left)
    d2, p2 = divide_and_conquer_closest_pair(right)
    d = min(d1, d2)

    # if they have the same distance then we need to join their pairs together
    pairs = []
    if d1 == d2:
        pairs += p1
        pairs += p2
    elif d1 < d2:
        pairs += p1
    elif d2 < d1:
        pairs += p2
    
    
    # calculate middle points
    lower_bound = median_x - d
    upper_bound = median_x + d
    middle = []

    for point in points:
        if point[0] >= lower_bound and point[0] <= upper_bound:
            middle.append(point)

    # sort middle points by y
    middle.sort(key=lambda x: x[1])
    
    # check all middle points for closest

    for i in range(len(middle)):
        j = i + 1
        while j < len(middle):

            if abs(middle[i][1] - middle[j][1]) > d:
                break

            dist = distance(middle[i], middle[j])
            if dist == d:
                pairs.append((middle[i], middle[j]))
            elif dist < d:
                d = dist
                pairs = [(middle[i], middle[j])]
            
            j += 1

    return d, list(set(pairs))


def closest_pair_rec(points: list[tuple[float, float]], points_y: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    n = len(points)
    # Solve if <= 3 points
    if n <= 3:
        pairs = []
        min_dist = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                d = distance(points[i], points[j])
                if d < min_dist:
                    min_dist = d
                    pairs = [(points[i], points[j])]
                elif d == min_dist:
                    pairs.append((points[i], points[j]))
        
        return min_dist, pairs
    
    # If there's more than 3 points
    # we will enter the recursive section

    # calculate left and right
    median_n = math.floor(n / 2)
    left = points[:median_n:]
    right = points[median_n::]
    
    # calculate median_x
    median_x = points[median_n][0]
    if n % 2 == 0:
        median_x = (points[median_n - 1][0] + median_x) / 2

    left_y = []
    right_y = []

    for point in points_y:
        if point[0] >= median_x:
            right_y.append(point)
        else:
            left_y.append(point)

    d1, p1 = closest_pair_rec(left, left_y)
    d2, p2 = closest_pair_rec(right, right_y)
    d = min(d1, d2)

    # if they have the same distance then we need to join their pairs together
    pairs = []
    if d1 == d2:
        pairs += p1
        pairs += p2
    elif d1 <= d2:
        pairs += p1
    elif d2 <= d1:
        pairs += p2

    # calculate middle points
    lower_bound = median_x - d
    upper_bound = median_x + d
    middle = []

    for point in points_y:
        if point[0] >= lower_bound and point[0] <= upper_bound:
            middle.append(point)
    
    # check all middle points for closest

    for i in range(len(middle)):
        j = i + 1
        while j < len(middle):

            if abs(middle[i][1] - middle[j][1]) > d:
                break

            dist = distance(middle[i], middle[j])
            if dist == d:
                pairs.append((middle[i], middle[j]))
            elif dist < d:
                d = dist
                pairs = [(middle[i], middle[j])]
            
            j += 1

    return d, list(set(pairs))

def enhanced_divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Recursively find the closest pair of points using a divide-and-conquer approach.

    Args:
        points (list[tuple[float, float]]): A list of 2D points where 
                                            each point is represented as a tuple (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The minimum distance between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """
    
    points.sort(key=lambda point: point[0])
    points_y_sorted = sorted(points, key=lambda point: point[1])
    
    min_distance, closest_pairs = closest_pair_rec(points, points_y_sorted)
    
    # Sort output pairs
    closest_pairs = sort_pairs(list({(tuple(pair[0]), tuple(pair[1])) for pair in closest_pairs}))

    return round(min_distance, 4), closest_pairs

def main():
    n = int(input("n:"))
    points = list(map(tuple, np.random.uniform(-100000, 100000, (n, 2)).tolist()))

    start = time.time()
    
    distance, pairs = enhanced_divide_and_conquer_closest_pair(points)

    print("Elapsed Time:",time.time() - start)
    print("Distance:", distance)
    print("Pairs:", pairs)



if __name__ == '__main__':
    main()

