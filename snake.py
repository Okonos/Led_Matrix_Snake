import max7219.led as led
from time import sleep

device = led.matrix()

class Segment:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def getCoords(self):
		return (self.x, self.y)

	def setCoords(self, x, y):
		self.x = x
		self.y = y

def setPixel(x, y):
	device.pixel(x, y, 1)

#def unset??

segments = []
segments.append(Segment(2, 4))
segments.append(Segment(2, 3))
segments.append(Segment(2, 2))

while True:
	for s in segments:
		setPixel(*(s.getCoords()))

	sleep(1)
	#class Point?
	#headCoords = segments[0].getCoords()
	segments.insert(0, segments.pop())
	#coords = segments[0].getCoords()
	#coords[1] += 1
	#segments[0].setCoords(*coords)
	segments[0].y = segments[1].y + 1

	device.clear()


sleep(3)
device.clear()

