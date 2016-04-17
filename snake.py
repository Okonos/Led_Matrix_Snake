import max7219.led as led
import RPi.GPIO as GPIO
from time import sleep

device = led.matrix()
GPIO.setmode(GPIO.BOARD)

def setPixel(x, y):
	device.pixel(x, y, 1)

#def unset??

def upCallback(channel):
	if snake.direction != Snake.Direction.DOWN:
		snake.direction = Snake.Direction.UP

def rightCallback(channel):
	if snake.direction != Snake.Direction.LEFT:
		snake.direction = Snake.Direction.RIGHT	

def downCallback(channel):
	if snake.direction != Snake.Direction.UP:
		snake.direction = Snake.Direction.DOWN

def leftCallback(channel):
	if snake.direction != Snake.Direction.RIGHT:
		snake.direction = Snake.Direction.LEFT

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
			self.segments[0] = self.Segment(head.x+1, head.y)	
		elif self.direction == self.Direction.DOWN:
			self.segments[0] = self.Segment(head.x, head.y+1)
		elif self.direction == self.Direction.LEFT:
			self.segments[0] = self.Segment(head.x-1, head.y)


snake = Snake()
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(35, GPIO.RISING, callback=leftCallback,bouncetime=300)
GPIO.add_event_detect(36, GPIO.RISING, callback=downCallback,bouncetime=300)
GPIO.add_event_detect(37, GPIO.RISING, callback=upCallback,bouncetime=300)
GPIO.add_event_detect(38, GPIO.RISING, callback=rightCallback,bouncetime=300)

try:
	while True:
		snake.draw()
		sleep(1)
		snake.move()
		device.clear()
except KeyboardInterrupt:
	GPIO.cleanup()
	sleep(3)
	device.clear()

GPIO.cleanup()
sleep(3)
device.clear()

