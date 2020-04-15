import telepot
import time


class telegram(object):
    """telegram notification"""

    def __init__(self, token):
        self.TOKEN = token  # identifica il nostro bot
        self.bot = telepot.Bot(self.TOKEN)  # inizializzo telepot
        self.chat_id = 'Nan'  # metto come Nan l'id della  chat finché qualcuno non mi indica di iniziare
        resp = self.bot.getUpdates()  # controllo l'ultimo messaggio
        if len(resp) == 0:
            self.ini = 0  # se c'è un messaggio dal bot o se non ci sono messaggi
        else:
            self.ini = int(resp[len(resp) - 1]['update_id'])  # altrimento prendo l'ultimo offset disponibile

    def starting_loop(self):  # loop di avvio. appena si avvia il servizio aspetta lo start
        while self.chat_id == 'Nan':
            self.start()

            # time.sleep(10)

    def start(self):  # controllo del messaggio start
        if self.ini == 0:  # se non ci sono messaggi inviati non serve aumentare l'offset
            response = self.bot.getUpdates()

        else:
            response = self.bot.getUpdates(offset=self.ini + 1)  # sennò mi prendo il successivo
        if len(
                response) == 0:  # in ogni caso considero il caso in cui non ci sono i messaggi. Da getUpdates ho una lista di dizionari(ogni dizionario è un messaggio con i suoi parametri)
            pass
        else:  # mi prendo l'ultimo dizionario e vedo se il testo 'start' c'è
            if response[len(response) - 1]['message']['text'] == 'Start':
                self.chat_id = response[0]['message']['chat']['id']  # se c'è mi prendo la chat_id che me lo ha scritto
                return self.chat_id

    def send_update(self, msg):
        if type(msg) == str:  # mando il messaggio e controllo se il messaggio è una stringa
            self.bot.sendMessage(self.chat_id, msg)
        else:
            self.bot.sendMessage(self.chat_id, str(msg))