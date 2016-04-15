import max7219.led as led
from time import sleep

device = led.matrix()

def setPixel(x, y):
	device.pixel(x, y, 1)

#def unset??

class Snake:
	class Direction:
		UP = 0
		RIGHT = 1
		DOWN = 2
		LEFT = 3

	class Segment:
		def __init__(self, x, y):
			self.x = x
			self.y = y

		def getCoords(self):
			return (self.x, self.y)

		def setCoords(self, x, y):
			self.x = x
			self.y = y
	
	def __init__(self):
		self.direction = self.Direction.DOWN
		self.segments = []
		self.segments.append(self.Segment(4, 3))
		self.segments.append(self.Segment(3, 3))
		self.segments.append(self.Segment(2, 3))

	def draw(self):
		for s in self.segments:
			setPixel(*(s.getCoords()))
	
	def move(self):
		head = self.Segment(*self.segments[0].getCoords())
		self.segments.insert(0, self.segments.pop())

		if self.direction == self.Direction.UP:
			self.segments[0] = self.Segment(head.x, head.y-1)
		elif self.direction == self.Direction.RIGHT:
			self.segments[0].x = self.Segment(head.x+1, head.y)	
		elif self.direction == self.Direction.DOWN:
			self.segments[0] = self.Segment(head.x, head.y+1)
		elif self.direction == self.Direction.LEFT:
			self.segments[0] = self.Segment(head.x-1, head.y)


snake = Snake()

while True:
	snake.draw()
	sleep(1)
	snake.move()
	device.clear()


sleep(3)
device.clear()

