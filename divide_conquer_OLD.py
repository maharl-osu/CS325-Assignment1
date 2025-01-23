import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file

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
    
    if len(points) == 1:
        return (float('inf'), [])
    elif len(points) <= 3:
        d = float('inf')
        pairs = []

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = distance(points[i], points[j])
                if dist < d:
                    d = dist
                    pairs = [(points[i], points[j])]
                elif dist == d:
                    pairs.append((points[i], points[j]))

        return d, pairs

    
    n = math.ceil(len(points) / 2)
    x_median = 0
    pairs = []
    points.sort(key=lambda x: x[0])

    if len(points) % 2 == 0:
        x_median = (points[n - 1][0] + points[n][0]) / 2
    else:
        x_median = points[n - 1][0]

    left = points[:n:]
    right = points[n::]

    d1, pts1 = divide_and_conquer_closest_pair(left)
    d2, pts2 = divide_and_conquer_closest_pair(right)

    if d1 < d2:
        pairs = pts1
    elif d1 > d2:
        pairs = pts2
    else:
        pairs = pts1 + pts2

    min_d = min(d1, d2)
    lower_bound = x_median - min_d
    upper_bound = x_median + min_d


    middle_pts = []
    for point in points:
        if point[0] >= lower_bound and point[0] <= upper_bound:
            middle_pts.append(point)
    
    middle_pts.sort(key=lambda x: x[1])

    min_d2 = float('inf')
    pairs2 = []

    for i in range(len(middle_pts)):
        for j in range(i + 1, len(middle_pts)):
            if abs(middle_pts[i][1] - middle_pts[i][1]) <= min_d:
                d = distance(middle_pts[i], middle_pts[j])
                if d < min_d2:
                    min_d2 = d
                    pairs2 = [(middle_pts[i], middle_pts[j])]
                elif d == min_d2:
                    pairs2.append((middle_pts[i], middle_pts[j]))


    if min_d < min_d2:
        return min_d, pairs
    elif min_d > min_d2:
        return min_d2, pairs2
    else:
        return min_d, list(set(pairs + pairs2))

if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        min_dist, closest_pairs = divide_and_conquer_closest_pair(points)

        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'ddnc_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
