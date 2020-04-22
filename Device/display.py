import time, datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import threading

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

        #metti a metodo
        self.print_logo()
        time.sleep(2)
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

        #inizializzo la variabile per stoppare il thread. La pongo a True perché così non devo entrare nel join(vedi successivamente, ora è nonrmale non capire)
        self.stop_thread=True


        # carico i font e ne definisco le dimensioni
        self.font = ImageFont.truetype('arial.ttf', 13)
        self.font1 = ImageFont.truetype('arial.ttf', 9)
        #istanzio il thread parallelo
        

    def close_all(self):
        #digli di printare arrivederci
        self.print_display("Spegnimento...", "Arrivederci!")
        #stampa l'animazione di logo
        self.disp.clear()
        self.disp.display()


    def print_display(self, text_y, text_b):
        ##per prima cosa mi sistemo le liste
             
        
        text_b=self.a_capo(text_b, self.width, self.font)
        
        pages_b=self.vertical_scrolling_b(text_b, 48, self.font) #48 son i pixel dello schermo blu in altezza
     
        pages_y=self.lateral_scrolling_y(text_y, self.width, self.font1)
        #ora le liste da stampare
  
        #qua è importante che sia a falso: se è a falso significa che c'è un thread in esecuzione quindi devo fermarlo -> pongo a True e aspetto che finsica il thread
        if self.stop_thread == False:
            self.stop_thread=True
            self.t.join()
        #avvio un thread parallelo per il display
        self.t = threading.Thread(target=self.scrolling, args=(pages_y, pages_b))
        self.t.start()




    def scrolling (self, pages_y, pages_b):
        y=0
        b=0
        if len(pages_b)==1 and len(pages_y)==1:
            #caso del no scrolling
            self.draw.rectangle((0,0,self.width, self.height), outline=0, fill=0)
            self.draw.text((0, 0), pages_y[y], font=self.font1, fill=255)
            self.draw.multiline_text((0, 16), pages_b[b], font=self.font, fill=255)
            self.disp.image(self.image)
            self.disp.display()
            self.stop_thread=True
        else:
            #caso dello scrolling
            #metto lo stop a falso e entro nel while
            self.stop_thread=False
            while self.stop_thread==False:
                self.draw.rectangle((0,0,self.width, self.height), outline=0, fill=0)
                self.draw.text((0, 0), pages_y[y], font=self.font1, fill=255)
                self.draw.multiline_text((0, 16), pages_b[b], font=self.font, fill=255)
                self.disp.image(self.image)
                self.disp.display()
                
                if b==len(pages_b)-1:
                    b=0
                else:
                    
                    b +=1

                if y==len(pages_y)-1:
                    y=0
                else:
            
                    y +=1
                time.sleep(10)






    def a_capo(self, string, len_max, font):
        ## funzione per andare a capo riferito al display. si va a capo con l'ultimo spazio disponibile

        #in input ha la stringa, la lunghezza massima per righa(in pixel) e il font
        #inizializzo gli indici
        index=-1
        prev_index=0
        w=0
        #prendo le misure del testo per vedere se ha bisogno sul serio della funzione
        real_w, h=self.draw.textsize(string, font=font)
        #ciclo finché non trovo il l'ultimo spazio prima della fine del display
        while w<len_max and real_w>len_max:
            prev_index=index #salvo l'indice precedente
            index=string.find(' ', index+1) 
            w, h=self.draw.textsize(string[0:index], font=font) #riprendo le dimensioni per vedere se sono arrivato alla fine
        #calcolando ora le dimensioni in pixel so se deve procedere ancora in modo ricorsivo (mi esce la lunghezza in pixel della riga più lunga)
        w, h=self.draw.textsize(string[prev_index:len(string)], font=font)
        
        if w>len_max:

            inp=string[prev_index:len(string)]
            #riparto con la funzione
            strin=self.a_capo(inp, len_max, font)
            #sostituisco la parte vecchia con quella con gli \n inseriti
            strl=list(string)
            strl[prev_index:len(string)]=list(strin)
            string="".join(strl)

        #sostituisco con il \n della attuale ricorsione
        list_string=list(string)
        #l'if mi serve per tenere conto che se è una parola sola non deve fare nulla
        if list_string[prev_index]==' ':
            list_string[prev_index]='\n'
        string="".join(list_string)
        return string



    def vertical_scrolling_b(self, text, height_max, font):
        ###faccio scorrere il testo se non entra nel display
        #ricorsione
        #inizializzazione
        index=-1
        prev_index=-1
        pages=[]
        start=0
        w, h_real=self.draw.textsize(text, font=font)
        #controllo se è necessario entrare nel while
        h=0
        if h_real>height_max:
            #controllo se h è minore del massimo (quindi se ho raggiunto la soglia per staccare) e se ha senso fare tutto   
            #l'ultimo controllo serve per capire se con l'ultima stringa inclusa
            while h<height_max:
                prev_index=index
                index=text.find('\n', index+1)


                w, h=self.draw.textsize(text[start:index], font=font) #riprendo le dimensioni per vedere se sono arrivato alla fine
        
            w, h=self.draw.textsize(text[prev_index+1:len(text)], font=font)
        
            stringa=self.vertical_scrolling_b(text[prev_index+1:len(text)], height_max, font)
        
            pages=pages + stringa
            pages.insert(0,text[start:prev_index])
        else:
            
            pages.append(text[prev_index+1:len(text)])  

        return pages



    def lateral_scrolling_y(self, text, len_max, font):
        ###faccio scorrere il testo piccolo giallo se non entra nei 128 pixel
        #come scrolling ma controllo gli spazi anziché gli a capo e tengo presente il parametro w anziché h
                ###faccio scorrere il testo se non entra nel display
        #ricorsione
        #inizializzazione
        index=-1
        prev_index=-1
        pages=[]
        start=0
        w_real, h=self.draw.textsize(text, font=font)
        
        #controllo se è necessario entrare nel while
        w=0
        #l'if serve a vedere se è necessario fare qualcosa
        if w_real>len_max:
            #controllo se h è minore del massimo (quindi se ho raggiunto la soglia per staccare) 
            while w<len_max: 
                prev_index=index
                index=text.find(' ', index+1)


                w, h=self.draw.textsize(text[start:index], font=font) #riprendo le dimensioni per vedere se sono arrivato alla fine

            
            #controllo la lunghezza del moncone: se è abbastanza lungo continuo sennò sono arrivato alla fine
            stringa=self.lateral_scrolling_y(text[prev_index+1:len(text)], len_max, font)
                
            pages=pages + stringa
            

            pages.insert(0,text[start:prev_index])
        else:
        
            
            pages.append(text[prev_index+1:len(text)])  
        
        return pages


    def print_logo(self):
        self.image = Image.open('pill2.png').convert('1')
        self.disp.image(self.image)
        self.disp.display()