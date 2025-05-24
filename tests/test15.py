# name: num_5_calculate_polygon_area
# label: 15
# method_tested: find_long_parameter_list()
# should_fail: False
def calculate_polygon_area(num_sides, side_length, apothem=None, circumradius=None):
    """
    Calculates the area of a regular polygon. Requires either the apothem or the circumradius.

    Args:
        num_sides (int): The number of sides of the polygon.
        side_length (float): The length of each side.
        apothem (float, optional): The distance from the center to the midpoint of a side. Defaults to None.
        circumradius (float, optional): The distance from the center to a vertex. Defaults to None.

    Returns:
        float: The area of the polygon.

    Raises:
        ValueError: If num_sides is less than 3, or if neither apothem nor circumradius is provided.

    Edge Cases:
        - num_sides less than 3 raises a ValueError.
        - Requires either apothem or circumradius to be provided.
    """
    if num_sides < 3:
        raise ValueError("Number of sides must be at least 3 for a polygon.")
    if apothem is None and circumradius is None:
        raise ValueError("Either the apothem or the circumradius must be provided.")

    if apothem is not None:
        area = 0.5 * num_sides * side_length * apothem
    else:
        import math

        area = 0.5 * num_sides * (circumradius**2) * math.sin(2 * math.pi / num_sides)
    return area
