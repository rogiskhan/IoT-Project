import time, datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

#display oled 0.96 pollici con risoluzione 128x64. In altezza i primi 16 pixel sono gialli e i successivi 48 sono blu
class display(object):
	def __init__(self):
		RST = 0 #da qui in poi inizializzo il display
		self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
		self.disp.begin()
		self.disp.clear()
		self.disp.display()
		self.width = self.disp.width
		self.height = self.disp.height

		#creo un'immagine da sfondo
		self.image = Image.new("1", (self.width, self.height), 255)
		# Creo un oggetto "draw"
		self.draw = ImageDraw.Draw(self.image)
		# disegno il contorno
		self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

 

		
		# Draw some shapes.
		# Definisco delle costanti per fare le forme
		padding = 2
		self.top = padding
		self.bottom = self.top-padding
		# Move left to right keeping track of the current x position for drawing shapes.
		self.x = 0

		

		# carico i font e ne definisco le dimensioni
		self.font = ImageFont.truetype('arial.ttf', 13)
		self.font1 = ImageFont.truetype('arial.ttf', 9)
		



	def print_med(self, ora, medicine ): #stampo il prossimo "appuntamento"
		bh=self.top+16 #definsico il punto dove c'è il blu
		stacco=0
		#stacco è il salto di 16 pixel. 16*3=48 che è l'altezza della parte blu
		self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
		self.draw.text((self.x, self.top), f'Prossima medicina: {ora}', font=self.font1, fill=255)#scrivo la parte sopra in giallo
		for i in medicine:
			#iterativamente scrivo le medicine da prendere (massimo 3 per pagina)
			self.draw.text((self.x, bh+stacco), i, font=self.font, fill=255)
			stacco=stacco+16
			self.disp.image(self.image)#carico l'immagine
			self.disp.display() #serve a scrivere sul display

		#devo aggiungere un modo per far girare le scritte se sono troppi farmaci. Magari posso aggiungere una icone di una lettere con vicino il numero dei medicinali tipo notifica

	def print_init(self):#come sopra ma scrivo un messaggio di inizializzazione
		self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
		self.draw.text((self.x, self.top), 'Benvenuto. Sto inizializzando...', font=self.font1, fill=255)
		self.draw.text((self.x, self.top+16), 'Scrivi Start ', font=self.font, fill=255)
		self.draw.text((self.x, self.top+32), 'al bot telegram', font=self.font, fill=255)
		self.draw.text((self.x, self.top+48), '@SamEsp8266bot', font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.display()


	def clear_disp(self):
		self.disp.clear()
