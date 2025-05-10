import math

def get_euclidean_distance_v1(point1, point2):
    """Calculates the Euclidean distance between two points (explicit loop)."""
    if not (len(point1) == len(point2) and all(isinstance(coord, (int, float)) for coord in point1 + point2)):
        raise ValueError("Points must be of the same dimension and contain numeric values.")
    squared_diffs = []
    for i in range(len(point1)):
        squared_diffs.append((point1[i] - point2[i]) ** 2)
    return math.sqrt(sum(squared_diffs))

def find_distance_between_points_v1(p1, p2):
    """Finds the distance between two points (using list comprehension)."""
    if not (len(p1) == len(p2) and all(isinstance(coord, (int, float)) for coord in p1 + p2)):
        raise ValueError("Points must have the same dimensions and numeric coordinates.")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))