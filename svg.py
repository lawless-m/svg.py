#!/usr/bin/python3

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scale(self, fx, fy):
        self.x = fx(self.x)
        self.y = fy(self.y)

    def translate(self, tp):
        self.x += tp.x
        self.y += tp.y

    def shrink(self, p):
        if p.x < self.x:
            self.x = p.x
        if p.y < self.y:
            self.y = p.y
        
    def expand(self, p):
        if p.x > self.x:
            self.x = p.x
        if p.y > self.y:
            self.y = p.y

    def dist(self, p):
        return math.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
    

class Style:
    def __init__(self, fill="none", stroke="black", stroke_width=1):
        self.attribs = {}
        self.set('fill', fill)
        self.set('stroke', stroke)
        self.set('stroke-width', stroke_width)

    def set(self, k, v):
        self.attribs[k] = v

    def write(self, io, units=""):
        io.write(' style="')
        for k in self.attribs:
            io.write(f"{k}:{self.attribs[k]}")
            if k == "stroke-width" and units != "":
                io.write(units)
            io.write(';')
            
        io.write('"')

class Shape:
    pass

class Circle(Shape):
    def __init__(self, center, radius, style=Style()):
        self.center = center
        self.radius = radius
        self.style = style

    def scale(self, fx, fy):
        self.center.scale(fx, fy)

    def translate(self, tp):
        self.center.translate(tp)

    def bounds(self):
        offset = self.radius + self.style.attribs['stroke-width'] / 2
        return Point(self.center.x - offset, self.center.y - offset), Point(self.center.x + offset, self.center.y + offset)
    
    def write(self, io, digits=2, units=""):
        io.write(f'<circle cx="{self.center.x:.{digits}f}{units}" cy="{self.center.y:.{digits}f}{units}" r="{self.radius:.{digits}f}{units}"')
        self.style.write(io, units=units)
        io.write(" />\n")

    def distance_to_boundary(self, p):
        d = math.sqrt((p.x - self.center.x)**2 + (p.y - self.center.y)**2)
        return d - self.radius if d > self.radius else -(self.radius - d)
    
    def print(self, end="\n"):
        print(f"Circle({self.center.x}, {self.center.y}, {self.radius})", end=end)

class Polyline(Shape):
    def __init__(self, points, style=Style()):
        self.points = points
        self.style = style

    def write(self, io, digits=2, units=""):    
        io.write(f'<polyline points="')
        for p in self.points:
            io.write(f'{p.x:.{digits}f}{units},{p.y:.{digits}f}{units} ')
        io.write('"')
        self.style.write(io, units=units)
        io.write(" />\n")

    def translate(self, tp):
        for p in self.points:
            p.translate(tp)

class Line(Shape):
    def __init__(self, startpoint, endpoint, style=Style()):
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.style = style

    def write(self, io, digits=2, units=""):    
        io.write(f'<line x1="{self.startpoint.x:.{digits}f}{units}" y1="{self.startpoint.y:.{digits}f}{units}" x2="{self.endpoint.x:.{digits}f}{units}" y2="{self.endpoint.y:.{digits}f}{units}"')
        self.style.write(io, units=units)
        io.write(" />\n")

    def translate(self, tp):
        self.startpoint.translate(tp)
        self.endpoint.translate(tp)

class Rect(Shape):
    def __init__(self, pt, size, rx=0, ry=0, style=Style()):
        self.origin = pt
        self.size = size
        self.rx = rx
        self.ry = ry
        self.style = style

    def translate(self, p):
        self.origin.translate(p)

    def bounds(self):
        offset = self.style.attribs['stroke-width'] / 2
        return Point(self.origin.x - offset, self.origin.y - offset), Point(self.origin.x + self.size.x + offset, self.origin.y + self.size.y + offset)
    
    def scale(self, fx, fy):
        self.origin.scale(fx, fy)
        self.size.scale(fx, fy)
        
    def write(self, io, digits=2, units=""):
        io.write(f'<rect x="{self.origin.x:.{digits}f}{units}" y="{self.origin.y:.{digits}f}{units}" width="{self.size.x:.{digits}f}{units}" height="{self.size.y:.{digits}f}{units}" rx="{self.rx:.{digits}f}{units}" ry="{self.ry:.{digits}f}{units}"')
        self.style.write(io, units=units)
        io.write(" />\n")

    def distance_to_boundary(self, p):      
        # Check if the point is inside the rectangle
        inside_x = self.origin.x <= p.x <= self.origin.x + self.size.x
        inside_y = self.origin.y <= p.y <= self.origin.y + self.size.y
        inside = inside_x and inside_y
        
        # Distances to the sides of the rectangle
        distance_left = p.x - self.origin.x
        distance_right = (self.origin.x + self.size.x) - p.x
        distance_top = p.y - self.origin.y
        distance_bottom = (self.origin.y + self.size.y) - p.y
        
        if inside:
            # Point is inside the rectangle, return the negative of the minimum distance to a side
            return -min(distance_left, distance_right, distance_top, distance_bottom)
        else:
            # Point is outside the rectangle, calculate the shortest distance to the rectangle's perimeter
            dx = max(self.origin.x - p.x, 0, p.x - (self.origin.x + self.size.x))
            dy = max(self.origin.y - p.y, 0, p.y - (self.origin.y + self.size.y))
            return (dx**2 + dy**2)**0.5

class Polyline(Shape):
    def __init__(self):
        pass

class SVG:
    def __init__(self):
        self.shapes = []

    def append(self, shape):
        self.shapes.append(shape)

    def merge(self, svg):
        for s in svg.shapes:
            self.shapes.append(s)
		
    def scale_shapes(self, fx, fy):
        for s in self.shapes:
            s.scale(fx, fy)
			
    def scale_functions(self, width, height, flip_y=False):
        xmin, ymin, xmax, ymax = self.bounds()
        xmx = xmax - xmin
        ymx = ymax - ymin
        scale = min(width, height) / min(xmx, ymx)
        fx = lambda x : scale * (x - xmin)
        fy = lambda y : height - (scale * (y - ymin) if flip_y else scale * (y - ymin))
        return fx, fy

    def bounds(self):
        pmin = Point(float('inf'), float('inf'))
        pmax = Point(-float('inf'), -float('inf'))
        for s in self.shapes:
            smin, smax = s.bounds()
            pmin.shrink(smin)
            pmax.expand(smax)

        return pmin, pmax
    
    def viewbox(self, digits=2, units=""):
        bmin, bmax = self.bounds()
        return f"{bmin.x:.{digits}f}{units} {bmin.y:.{digits}f}{units} {(bmax.x-bmin.x):.{digits}f}{units} {(bmax.y-bmin.y):.{digits}f}{units}"
	
    def write(self, io, width, height, viewbox="", stylesheet="", units=""):
        if viewbox != "" :
            viewbox = f' viewBox="{viewbox}"'
        io.write(f'<svg width="{width}{units}" height="{height}{units}"{viewbox} xmlns="http://www.w3.org/2000/svg">\n')
        if stylesheet != "":
            io.write('<style>\n@import url({stylesheet}.css)\n</style>\n')

        for s in self.shapes:
            s.write(io, units=units)

        io.write("</svg>")

    def write_html(self, io, width, height, viewbox="", stylesheet="", units=""):
        open_html(io)
        self.write(io, width, height, viewbox, stylesheet, units)
        close_html(io)

    def translate(self, p):
        for s in self.shapes:
            s.translate(p)


def open_html(io):
    io.write("<!DOCTYPE html>\n<html>\n<body>\n<div>\n")

def close_html(io):
    io.write("</div>\n</body>\n</html>\n")

if __name__ == "__main__":
    svg = SVG()
    svg.append(Circle(0,0,10))
    with open("/tmp/svgtest.html", "w+") as io:
        svg.write_html(io, 100, 100, svg.viewbox())

