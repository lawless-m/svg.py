from svg import Point, SVG, Polyline, Style
from Logo import Logo

ab = 10

hex = Logo(Point(0,0)) # kk

hex.turn(90).fwd(ab) # kk -> ak
hex.turn(72).fwd(ab) # ak -> a
hex.turn(72).fwd(ab) # a -> b
hex.turn(72).fwd(ab) # b -> c

hex.bearing = 90

hex.turn(72).fwd(ab) # ak -> a
hex.turn(72).fwd(ab) # a -> b
hex.turn(72).fwd(ab) # b -> c
hex.turn(72).fwd(ab) # b -> c

svg = SVG()
p = Polyline(hex.points)

svg.append(p)

with open('hex.html', 'w+') as io:
	svg.write_html(io, 500, 500, svg.viewbox())



