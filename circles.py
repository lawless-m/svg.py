#!/usr/bin/python3

import random
from svg import *

def rpoint(pmin, pmax):
    return Point(pmin.x + (pmax.x-pmin.x) * random.random(), pmin.y + (pmax.y-pmin.y) * random.random())

def check_against_svg(svg, c, space=5):
    for s in svg.shapes:
        if isinstance(s, Circle):
            d = s.distance_to_boundary(c.center) - c.radius
            if d < space:
                return False
        if isinstance(s, Rect):
            d = s.distance_to_boundary(c.center) + c.radius
            if d > 0 or -d < space :
                return False
    return True

def add_circles(svg, pmin, pmax, n, r, space=5, tries=10000):
    for i in range(0,n):
        t = 0
        while t < tries:
            p = rpoint(pmin, pmax)
            c = Circle(p, r)
            if check_against_svg(svg, c, space):
                svg.append(c)
                t = tries
            else:
                t += 1

def create_tab(position, height, width):
    svg = SVG()
    svg.append(Rect(Point(0,0),Point(width,height)))
    svg.append(Circle(Point(width/2, 15), 3))
    
    add_circles(svg, Point(10, 20), Point(30, height-10), n=5, r=8, space=4)
    add_circles(svg, Point(10, 20), Point(30, height-10), n=10, r=5, space=4)
    add_circles(svg, Point(10, 20), Point(30, height-10), n=15, r=3, space=4)

    svg.translate(position)
    return svg

def write_page(svg, page):
    with open(f"/home/matt/circles/circles_{page}.svg", "w+") as io:
        svg.write(io, 210, 297, "0mm 0mm 210mm 297mm", units="mm")

def create_tabs():
    svg = SVG()
    offset = 10
    tabw = 35
    spacing = tabw
    x = offset
    page = 0
    pagew = 210
    nextorigin = pagew
    for height in [235, 290, 275, 260, 285, 240, 271, 231]: # [270, 280, 250, 235, 290, 275, 260, 285, 240, 271, 231]
        svg.merge(create_tab(Point(x,3), height, tabw))
        if x + spacing + tabw >= nextorigin :
            page += 1
            x = pagew * page + 5 + offset
            nextorigin += pagew
        else:
            x += spacing

    write_page(svg, 2)

"""
c = Circle(0,0,10)
print(c.distance_to_boundary(0,5))
print(c.distance_to_boundary(0,15))
"""

create_tabs()