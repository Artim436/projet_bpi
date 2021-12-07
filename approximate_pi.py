#!/usr/bin/env python3

""" program approximate_pi.py """

import sys
import random as rd

def in_circle(point):
    """ is the point in the circle?"""
    if point[0]**2+point[1]**2 <= 1:
        return True
    return False

def draw_function(number_points):
    """ main function for approximate_pi"""
    for _ in range(number_points):
        point = [rd.uniform(-1, 1), rd.uniform(-1, 1)]
        yield [point, in_circle(point)]

def main(number_points):
    """main function but faster"""
    cpt = 0
    for _ in range(number_points):
        point = [rd.uniform(-1, 1), rd.uniform(-1, 1)]
        if in_circle(point):
            cpt += 1
    return (cpt/number_points)*4

if __name__ == "__main__":
    print(main(int(sys.argv[1])))
 