from telegram import *  # mia classe
import time
from gpiozero import Button, RGBLED, Buzzer
from colorzero import Color  # serve per i colori del led


# manca il buzzer e il led come metodi
class notifier(object):
    def __init__(self, pin_button, token, pinbuzzer, pinr, ping,
                 pinb):  # inizializzazione GPIO e comunicazione con il bot di telegram
        self.rgb_led = RGBLED(pinr, ping, pinb, pwm=True)  # istanzio il led
        self.pin = pin  # pin del buzzer
        self.buzzer = Buzzer(pinbuzzer)  # istanzio il buzzer
        self.tg = telegram(token)  # istanzion telegram
        self.pushed = 0  # setto a zero una variabile per il loop e la callback
        self.rgb_led.value = Color(
            'green')  # metot il led verd, questa è la prima funzione che viene eseguita all'avvio del pacchetto
        self.tg.starting_loop()  # cerco il messaggio start all'avvio dell'applicazione. Va messo in init perché va tutto inizializzato all'avvio del sistema

    def my_callback(self):  # callback pulsante premuto
        self.pushed = 1

    # crit è una soglia di messaggio entro cui devo mandare la notifica speciale col buzzer
    def message_loop(self, msg, freq, crit,
                     rit):  # freq è ogni quanto mando il messaggio sarebbe scorretto ma è più intuitivo espresso in minuti
        # rit è il ritardo massimo tra un turno e l'altro meno 15 minuti
        button = Button(self.pin, bounce_time=100,
                        pull_up=False)  # istanzio il pulsante. Devo farlo a ogni volta sennò non è "resettato"
        self.rgb_led.value = Color('magenta')  # colore di qunado va presa la pillola
        button.when_pressed = self.my_callback  # interrupt del pulsante
        start = time.time()  # inizio il conto del ritardo
        count = 0  # inizio il conteggio dei messaggi
        while self.pushed == 0:  # loop di invio del messaggio
            self.tg.send_update(msg)
            count = count + 1
            if count > crit:  # se sto nel crit avvio led rosso e buzzer
                self.buzzer_sound(freq * 60)
                self.rgb_led.value = Color('red')
            for i in range(int(freq * 60)):  # polling per il conteggio del tempo tra un messaggio e l'altro
                lap = time.time() - start
                if self.pushed == 0 and lap < rit:  # controllo che una delle due condizioni (pulsante e tempo passato <un'ora)
                    time.sleep(1)
                else:
                    self.pushed = 1  # metto la condizione anche qua perché così se entro nell'else tramite tempo esco dal while
                    break
        end = time.time()  # ha premo il pulsante sono fuori dal loop finisco il conteggio del ritardo
        self.pushed = 0
        self.rgb_led.value = Color('green')  # quando ha preso il medicinale metto il colore verde
        if count > 1:  # solo se l'utente si fa pregare considero il ritardo
            dt = end - start  # ritardo
            m, s = divmod(dt, 60)  # conversione in minuti e secondi
            prompt = (f'Sei in ritardo di {int(m)} minuti e {int(s)} secondi!')
            self.tg.send_update(prompt)
            dt = m
            return dt
        else:
            dt = 0  # se ho mandato solo un messaggio considero la cosa buona e conto ritardo nullo
            return dt

    def buzzer_sound(self, tim):  # tim è il tempo che il buzzer suona
        periodo = int(tim / 1)  # lascio 1 perché mi ricordo che divido per la somma del tempo on e off
        self.buzzer.beep(on_time=0.5, off_time=0.5, n=periodo, background=True)

