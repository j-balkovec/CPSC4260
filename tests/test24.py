# name: num_4_get_rectangle_area_v2_find_cuboid_volume_v2
# label: 24
# method_tested: find_duplicated_code()
# should_fail: False
def get_rectangle_area_v2(side_a, side_b, magnification=1.0):
    """Gets the area of a rectangle."""
    if side_a < 0 or side_b < 0:
        raise ValueError("Side A and Side B must be non-negative.")
    return side_a * side_b * magnification

def find_cuboid_volume_v2(breadth, tallness, thickness, zoom=1.0):
    """Finds the volume of a cuboid."""
    if breadth < 0 or tallness < 0 or thickness < 0:
        raise ValueError("Breadth, Tallness, and Thickness must be non-negative.")
    return breadth * tallness * thickness * zoom