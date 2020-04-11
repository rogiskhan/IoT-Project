# #prototipi
import time



# #funzioni che prende in input il piano e lo ordina per orario
class dati(object):
    
    def init(self):
        pass
    
        
    def riordina(self, piano): #riordino il piano. Elena forse riesce a renderla inutile
        ora=[]
        med=[]
        #prendiamo il valore della chiave orario e facciamo il sort classico
        piano_ordinato=sorted(piano, key=lambda i: i['orario'])
        for orari in piano_ordinato:
            ora.append(orari['orario'])
        ora = dict.fromkeys(ora) 
        for time in ora.keys():
            for time2 in piano_ordinato:
                if time==time2['orario']:
                    med.append(time2['medicina'])
            ora[time]=med
            med=[]
        
        return ora
    #trova prima ora del pian disponibile per medicine da prendere nel momento in cui viene chiamata
    def find_first(self, ora):
        hour=int(time.strftime("%H"))+1
        minute=int(time.strftime("%M"))
        chiavi=[]
        flag=0
        for key in ora.keys():
            chiavi.append(key)
        chiavi.sort()
        for i in range (len(chiavi)):
            chiavi1=chiavi[i].split(':')
            if int(chiavi1[0])<hour: 
              pass
            elif int(chiavi1[0])==hour and int(chiavi1[1])<=minute:
              pass

            else:
              flag=1
              break

            if flag==0: #per scavalcare il giorno sennò non fa
              i=0
        return i,chiavi
    
    #controlla se è ora
    def is_now(self,prossima_ora): #prossima_ora è chiavi[i]
        hour=int(time.strftime("%H"))+1
        minute=int(time.strftime("%M"))
        tmp=prossima_ora.split(":")
        if int(tmp[0])==hour and int(tmp[1])==minute:
            return True
        else:
            return False
        #out boolean input è stringa   

    def switch(self, score, orario):
        scor=score[orario]
        if scor<2:
          f=20 #frequenza dei messaggi in minutiS
          crit=1000 #infinito

        elif scor<5:
          f=15
          crit=2#dopo il terzo messaggio
        elif scor<7:
          f=10
          crit=2

        elif scor<=10:
          f=7
          crit=2

        return f, crit     

    def ritmax(self, now, next): ##now e next sono stringhe 
        tmp=now.split(":")
        tmp1=next.split(":")
        nowm=int(tmp[0])*60+int(tmp[1])
        nextm=int(tmp1[0])*60+int(tmp1[1])
        rit=(nextm-nowm-15)*60

        return rit

    def ritardi_update(self, piano, ritardi):
      #funzione per aggiornare il dizionario dei ritardi
      rita=[] #lista delle ore dei ritardi (ore vecchie)
      pian=[] #lista per le ore del piano (ore nuove)
      for i in piano.keys():
        pian.append(i)
      for j in ritardi.keys():
        rita.append(j)
      dele=list(set(rita) - set(pian)) #orari da eliminare
      add=list(set(pian) - set(rita)) #orari da aggiungere
      for keys in dele:
        del ritardi[keys]
      for keys in add:
        ritardi.update({keys:0})
      return ritardi
                  
                
                
                
                
                
##algoritmo: serie di soglie (bottone,pericolosità...) se sopra o sotto so quale allarme
#attivare. In più valuto ritardo medio sulla fascia oraria (se mi scordo spesso in quell'ora 
#notifica sempre più impellente). Per ogni fascia oraria mi calcolo uno score per ogni medicinale
#prendo max perchè più urgente. Da lì ho look up table switch case che mi dice quale allarme usare
              
    def algoritmo(self,piano,farmaci, ritardi):
        w1=1 #peso ritardo
        w2=5 #peso pericolosità
        #ricorda di inizializzare i pesi w prima apriori
        massimo = w1*60 + w2*10
        minimo = w2
        scor1_diz={} #primo score con ora:score legato ai ritardi e pericolosità
        for orario in piano.keys():
            ritardo=ritardi[orario]
            if ritardo>60:
              ritardo=60
            farmaci_selected=piano[orario]
            scoretmp1=[]
            for farmaco in farmaci_selected:
                pericolosita=farmaci[farmaco]['pericolosità']
                tmp=w1*ritardo + w2*pericolosita
                scoretmp1.append(tmp)
            score1=max(scoretmp1)
            score1=round((score1-minimo)*10/(massimo-minimo))
            scor1_diz.update({orario: score1})
            
        return scor1_diz
