#!/usr/local/bin/python

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
                svg.append(Line(Point(c.center.x-1, c.center.y), Point(c.center.x+1, c.center.y)))
                svg.append(Line(Point(c.center.x, c.center.y-1), Point(c.center.x, c.center.y+1)))
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
    with open(f"circles_{page}.svg", "w+") as io:
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
    for height in [210, 250, 260, 220, 155, 235, 260, 260, 220, 260,235,80]:
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


def exspace(x):
    pmin = Point(5, 3)
    pmax = Point(40,12)
  
    m = (pmax.y - pmin.y) / (pmax.x - pmin.x) 
    c = pmin.y - m * pmin.x
    return x * m + c


def ender():
	svg = SVG()
	svg.append(Rect(Point(0,0), Point(100,40)))
	cnt = 0
	while cnt < 35:
		p = rpoint(Point(3,5), Point(95, 37))
		c = Circle(p, 1, Style(stroke_width=0.5))
		if check_against_svg(svg, c, exspace(c.center.y)):
			svg.append(c)
			cnt += 1
			print(cnt)
	return svg

def double_ender():
    svg = SVG()
    e = ender()
    e.translate(Point(0, 50))
    svg.merge(e)
    e = ender()
    svg.merge(e)

    write_page(svg, 'ender')

double_ender()

#create_tabs()

