from copy import deepcopy
from queue import PriorityQueue
from Point import Point
#from Map import Map
import math

'''AIModule Interface
createPath(map map_) -> list<points>: Adds points to a path'''
class AIModule:

	def createPath(self, map_):

		path = []
		explored = []
		# Get starting point
		path.append(map_.start)
		current_point = deepcopy(map_.start)

		pass

'''
A sample AI that takes a very suboptimal path.
This is a sample AI that moves as far horizontally as necessary to reach
the target, then as far vertically as necessary to reach the target.
It is intended primarily as a demonstration of the various pieces of the
program.
'''
class StupidAI(AIModule):

	def createPath(self, map_):
		path = []
		explored = []
		# Get starting point
		path.append(map_.start)
		current_point = deepcopy(map_.start)

		# Keep moving horizontally until we match the target
		while(current_point.x != map_.goal.x):
			# If we are left of goal, move right
			if current_point.x < map_.goal.x:
				current_point.x += 1
			# If we are right of goal, move left
			else:
				current_point.x -= 1
			path.append(deepcopy(current_point))

		# Keep moving vertically until we match the target
		while(current_point.y != map_.goal.y):
			# If we are left of goal, move right
			if current_point.y < map_.goal.y:
				current_point.y += 1
			# If we are right of goal, move left
			else:
				current_point.y -= 1
			path.append(deepcopy(current_point))

		# We're done!
		return path

class Djikstras(AIModule):

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path


# PASSES ALL SEEDS
class AStarExp(AIModule):

	def createPath(self, map_):

		#-------------------------------------#
		def get_heuristic_expo(node_x, node_y, goal_x, goal_y, h0, h1):
			h_n = 0
			delta_x = max(abs(node_x - goal_x), abs(node_y - goal_y))
			delta_h = h1 - h0

			if delta_h < 0: # Downhill
				h_n = (2**(delta_h/delta_x)) * delta_x

			elif delta_h == 0: # Same height
				h_n = delta_x

			elif delta_h > 0: # Uphill
				h_n = math.sqrt((delta_h**2)+(delta_x**2))

			else:
				print("Error")
				pass

			return h_n
		#-------------------------------------#


		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]

				# Get the heuristic function
				height0 = map_.getTile(neighbor.x, neighbor.y)
				height1 =  map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
				h_n = get_heuristic_expo(neighbor.x, neighbor.y, map_.getEndPoint().x, map_.getEndPoint().y, height0, height1)

				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt + h_n # Add the heuristic
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path


# PASSES ALL SEEDS
class AStarDiv(AIModule):

	def createPath(self, map_):

		#-------------------------------------#
		def get_heuristic_div(node_x, node_y, goal_x, goal_y):

			delta_x = max(abs(node_x - goal_x), abs(node_y - goal_y))
			h_n = delta_x/2
			return h_n

			'''
			if delta_h < 0: # Downhill
				if delta_h > delta_x: # If height is greater than distance
					summation = 0
					for i in range(0, delta_h):
						summation = summation + (i/(i+2))
					h_n = (delta_x/delta_h) * summation

				elif delta_h < delta_x: # If height is less than distance
					summation = 0
					for i in range(0, delta_h):
						summation = summation + (i/(i+2))
					h_n = (delta_h/delta_x) * summation

				elif delta_h == delta_x: # If height is equal to distance
					summation = 0
					for i in range(0, delta_h):
						summation = summation + (i/(i+2))
					h_n = summation

				else: 
					print("Error 1")
					pass
				

			elif delta_h == 0: # Same height
				h_n = delta_x

			elif delta_h > 0: # Uphill
				if delta_h > delta_x: # If height is greater than distance
					h_n = delta_x * (delta_h / delta_x)

				elif delta_h < delta_x: # If height is less than distance
					h_n = delta_x * (delta_x / delta_h)
				
				elif delta_h == delta_x: # If height is equal to distance
					h_n = delta_x

				else:
					print("Error 2")
					pass

			else:
				print("Error 3")
				pass

			return h_n
			'''

		#-------------------------------------#

		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]

				# Get the heuristic function
				#height0 = map_.getTile(v.x, v.y)
				#height1 = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
				h_n = get_heuristic_div(v.x, v.y, map_.getEndPoint().x, map_.getEndPoint().y)

				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt + h_n # add the heuristic
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path


# USE PREVIOUS HEURISTIC AND MAKE MORE TIME EFFICIENT
class AStarMSH(AIModule):

	def createPath(self, map_):

		#-------------------------------------#
		def get_heuristic_msh(node_x, node_y, goal_x, goal_y, h0, h1):

			h_n = 0
			delta_x = max(abs(node_x - goal_x), abs(node_y - goal_y))
			delta_h = h1 - h0
			
			if delta_h < 0: # Downhill
				h_n = (2**(delta_h/delta_x)) * delta_x

			elif delta_h == 0: # Same height
				h_n = delta_x

			elif delta_h > 0: # Uphill
				h1_n = math.sqrt((delta_h**2)+(delta_x**2))
				h2_n = (2**(delta_h/delta_x)) * delta_x
				h_n = max(h1_n, h2_n, 2*delta_h)

			else:
				print("Error")
				pass
			
			return h_n
		#-------------------------------------#
		

		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]

				# Get the heuristic function
				height0 = map_.getTile(neighbor.x, neighbor.y)
				height1 =  map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
				h_n = get_heuristic_msh(neighbor.x, neighbor.y, map_.getEndPoint().x, map_.getEndPoint().y, height0, height1)

				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt + h_n # Add the heuristic
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path















































