# name: num_3_calculate_area_rectangle_v1_compute_volume_cuboid_v1
# label: 23
# method_tested: find_duplicated_code()
# should_fail: False
def calculate_area_rectangle_v1(length, width, scale=1.0):
    """Calculates the area of a rectangle."""
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return length * width * scale

def compute_volume_cuboid_v1(base, height, depth, factor=1.0):
    """Computes the volume of a cuboid."""
    if base < 0 or height < 0 or depth < 0:
        raise ValueError("Base, height, and depth cannot be negative.")
    return base * height * depth * factor