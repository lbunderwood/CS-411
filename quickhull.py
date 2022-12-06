# quickhull.py
# Created by Luke Underwood 2022-11-02
# implementation of quickhull algorithm for finding a convex hull

import math
import random
import time
import matplotlib.pyplot as plt

# The first two inputs form a line, and the function returns a number > 0 
# if the point given by the third input is on one side, < 0 if it is on the other.
def findside(line_start, line_end, point):
    side = (line_end[0] - line_start[0]) * (line_start[1] - point[1])
    side = side - (line_start[0] - point[0]) * (line_end[1] - line_start[1])
    return side


# recursive quickhull implementation
def hullrecurse(points, line_start, line_end, side):
    
    furthest_idx = -1 # updated in loop to be index of element furthest from the line
    max_dist = 0      # updated in loop to be distance from line to points[furthest_idx]

    # find point furthest from line on the side indicated by side
    for i in range(len(points)):
        
        # point_side will be > or < 0 depending on which side of the line the point is
        point_side = findside(line_start, line_end, points[i])
 
        # dist is distance from line to point
        dist = abs(point_side)
        dist = dist / math.sqrt((line_end[0] - line_start[0]) ** 2 + (line_end[1] - line_start[1]) ** 2)
        
        # if side and point_side are both < 0 or both > 0, and dist is new highest, update variables
        if side * point_side > 0 and dist > max_dist:
            furthest_idx = i
            max_dist = dist

    # BASE CASE: no points found, add both points to hull
    if furthest_idx == -1:
        return {line_start, line_end}

    # RECURSIVE CASE: recurse on the lines from the old points to the new point 
    #                 using side = opposite of the side that the other old point is on
    hull = hullrecurse(points, line_start, points[furthest_idx], -1 * findside(line_start, points[furthest_idx], line_end)) 
    return hull | hullrecurse(points, line_end, points[furthest_idx], -1 * findside(line_end, points[furthest_idx], line_start)) 



# sets up and calls recursive function
def quickhull(points):
    
    # find points with min and max x
    min_idx = max_idx = 0
    for i in range(len(points)):
        if points[i][0] < points[min_idx][0]:
            min_idx = i
        if points[i][0] > points[max_idx][0]:
            max_idx = i

    # recurse and join results
    hull = hullrecurse(points, points[min_idx], points[max_idx], 1)
    return hull | hullrecurse(points, points[min_idx], points[max_idx], -1)


# generates list of points of size n
def getpoints(n):
    points = []
    for i in range(n):
        points.append((random.random(), random.random()))
    return points


# calling code
def main():
    
    for n in (10, 100, 1000, 10000):
        points = getpoints(n)

        print("\n\n\n\nInput: ", points)
        start_time = time.time()
        hull = quickhull(points)
        end_time = time.time()
        print("\n\n\n\nOutput: ", hull)
        print(f"\n\nTime for n = {n} is {end_time - start_time}")
        hull = list(hull)
        for i in range(len(hull) - 1):
            closest = -1
            closest_dist = 2
            for j in range(i + 1, len(hull)):
                dist = math.sqrt((hull[i][0] - hull[j][0]) ** 2 + (hull[i][1] - hull[j][1]) ** 2)
                if closest == -1 or dist < closest_dist:
                    closest = j
                    closest_dist = dist
            temp = hull[i + 1]
            hull[i + 1] = hull[closest]
            hull[closest] = temp

        x_hull = [p[0] for p in hull]
        y_hull = [p[1] for p in hull]
        x = [p[0] for p in points]
        y = [p[1] for p in points]

        plt.scatter(x, y)
        for i in range(len(hull)):
            if i == len(hull) - 1:
                plt.plot([x_hull[i], x_hull[0]], [y_hull[i], y_hull[0]])
            else:
                plt.plot([x_hull[i], x_hull[i+1]], [y_hull[i], y_hull[i+1]])
        plt.show()
        


main()

