
import math
from svg import Point

class Logo:
	def __init__(self, origin:Point, bearing=0):
		self.points = [origin.copy()]
		self.bearing = bearing
		self.position = origin.copy()
	
	def turn(self, angle):
		self.bearing += angle
		return self

	def fwd(self, distance):
		self.points.append(self.position.move(distance, self.bearing).copy())
		return self

		
	
		
