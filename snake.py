import max7219.led as led
import RPi.GPIO as GPIO
from time import sleep
from random import randrange

device = led.matrix()
device.brightness(3)
buffLen = len(device._buffer) - 1
GPIO.setmode(GPIO.BOARD)

def setPixel(x, y):
	device.pixel(x, y, 1)

def clearPixel(x, y):
	device.pixel(x, y, 0)

def upCallback(channel):
	if snake.direction not in (Snake.Direction.DOWN, Snake.Direction.UP):
		snake.instantTurningMovement(Snake.Direction.UP)

def rightCallback(channel):
	if snake.direction not in (Snake.Direction.LEFT,Snake.Direction.RIGHT):
		snake.instantTurningMovement(Snake.Direction.RIGHT)

def downCallback(channel):
	if snake.direction not in (Snake.Direction.UP, Snake.Direction.DOWN):
		snake.instantTurningMovement(Snake.Direction.DOWN)

def leftCallback(channel):
	if snake.direction not in (Snake.Direction.RIGHT,Snake.Direction.LEFT):
		snake.instantTurningMovement(Snake.Direction.LEFT)

class Food:
	def __init__(self):
		self.location = 0 
		self.spawn()

	def spawn(self):
		colliding = True
		while colliding:	
			colliding = False
			x = randrange(0, buffLen)
			y = randrange(0, buffLen)
			self.location = (x, y)
			for segment in snake.segments:
				if self.location == segment.getCoords(): 
					colliding = True
					break

	def draw(self):
		setPixel(*self.location)
	

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
		self.collided = False
		self.foodConsumed = False
		self.segments = []
		self.segments.append(self.Segment(4, 3))
		self.segments.append(self.Segment(3, 3))
		self.segments.append(self.Segment(2, 3))
		self.segments.append(self.Segment(1, 3))
		#self.segments.append(self.Segment(0, 3))

	def draw(self):
		# Only head changed place
		setPixel(*self.segments[0].getCoords())
		
	def checkCollisions(self, head):
		# Wall collision
		if (
			head.y == 0 and self.direction == self.Direction.UP or
			head.y == buffLen and self.direction == self.Direction.DOWN or
			head.x == 0 and self.direction == self.Direction.LEFT or
			head.x == buffLen and self.direction == self.Direction.RIGHT
			):
			return True

		return False
	
	def move(self):
		head = self.Segment(*self.segments[0].getCoords())

		if self.checkCollisions(head):
			self.collided = True
			return

		self.segments.insert(0, self.segments.pop())
		tail = self.segments[0].getCoords()
		
		if self.direction == self.Direction.UP:
			self.segments[0] = self.Segment(head.x, head.y-1)
		elif self.direction == self.Direction.RIGHT:
			self.segments[0] = self.Segment(head.x+1, head.y)	
		elif self.direction == self.Direction.DOWN:
			self.segments[0] = self.Segment(head.x, head.y+1)
		elif self.direction == self.Direction.LEFT:
			self.segments[0] = self.Segment(head.x-1, head.y)

		# Segments collision
		for segment in self.segments[1:]:
			if self.segments[0].getCoords() == segment.getCoords():
				self.collided = True

		# Food collision/consumption
		if self.segments[0].getCoords() == food.location:
			self.segments.insert(0, self.Segment(*food.location))
			self.foodConsumed = True

		# Clear the tail if it's not consumed food
		if self.segments[-1].getCoords() != tail:
			clearPixel(*tail) 

	def instantTurningMovement(self, direction):
		self.direction = direction
		self.move()
		self.draw()


snake = Snake()
# Initial draw
for segment in snake.segments:
	setPixel(*segment.getCoords())
food = Food()
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(35, GPIO.RISING, callback=leftCallback,bouncetime=300)
GPIO.add_event_detect(36, GPIO.RISING, callback=downCallback,bouncetime=300)
GPIO.add_event_detect(37, GPIO.RISING, callback=upCallback,bouncetime=300)
GPIO.add_event_detect(38, GPIO.RISING, callback=rightCallback,bouncetime=300)

try:
	while not snake.collided:
		if snake.foodConsumed:
			snake.foodConsumed = False
			food.spawn()
		snake.draw()
		food.draw()
		sleep(1)
		snake.move()
except KeyboardInterrupt:
	GPIO.cleanup()
	sleep(3)
	device.clear()

GPIO.cleanup()
sleep(3)
device.clear()

