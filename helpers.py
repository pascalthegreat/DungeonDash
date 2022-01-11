import numpy as np
import math

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


# Return true if line segments AB and CD intersect
def intersect(l1, l2):
    return ccw(l1[0], l2[0], l2[1]) != ccw(l1[1], l2[0], l2[1]) and ccw(l1[0], l1[1], l2[0]) != ccw(l1[0], l1[1], l2[1])


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def get_angle(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    if x1 == x2:
        if y2 > y1:
            angle = 180
        else:
            angle = 0
    else:
        to_add = 270 if x2 < x1 else 90
        angle = math.degrees(math.atan((y2 - y1) / (x2 - x1))) + to_add
    return angle

