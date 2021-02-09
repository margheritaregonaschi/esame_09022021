##ESAME LAB DI PROGRAMMAZIONE 09/02/2021
##REGONASCHI MARGHERITA matricola: EC2100744
##corso di laurea: Statistica e Informatica per l'azienda...


#Creo la classe ExamException
class ExamException(Exception):
    pass

#Creo la classe CSVTimeSeriesFile
class CSVTimeSeriesFile:

    #la classe deve essere istanziata sul nome del file tramite la variabile name
    def __init__(self, name):
        self.name = name

    def get_data(self):
    #la classe deve avere un metodo che mi ritorni una lista di liste 
    #primo elemento della lista = epoch; sec elemento della lista = temperature
        #Inizializzo una lista vuota per salvare i valori
        #righe è la mia lista finale che comprenderà altre liste
        righe = []

        #Provo ad aprire il file. Se non ci riesco, avverto del'errore poi faccio terminare il programma (Errore "un-recoverable")
        try:
            file = open(self.name, 'r')
        except Exception as e:
            #alzo l'eccezione            
            raise ExamException('Errore nella lettura del file: “{}”'.format(e))
        
        
        #Leggo il file linea per linea
        for line in file:
            
            #faccio lo split di ogni linea sulla virgola
            elementi = line.split(',')

            #controllo che questa riga abbia 2 colonne, se non ha due colonne significa che la riga non è conforme con le altre: la salto e proseguo
            if len(elementi) != 2:
                continue

            #se non processo l'intestazione...
            if elementi[0] != 'epoch':
                   
                #setto epoch e temperature
                epoch  = elementi[0]
                temperature = elementi[1]
                
                #Converto epoch in int
                #Un valore di temperatura non numerico (o vuoto o nullo) non deve essere accettato ma il programma deve procedere (Errore "recoverable")
                try:  
                    epoch = int(float(epoch)) #converto epoch in float dopo faccio il cast a int in modo da eliminare la parte decimale
                except Exception as e:
                    #Se viene alzata un'eccezione non si esegue l'append ma proseguo con il ciclo
                    continue

                #Converto temperature in float
                try:
                    temperature = float(temperature)
                except Exception as e:
                    continue

                #creo una lista (riga) che mi salva riga per riga epoch e temperature
                riga = [epoch, temperature]
                #aggiungo a righe --> riga poichè righe è una lista di liste
                righe.append(riga)

        # Chiudo il file
        file.close()

        #richiamo il metodo validazione_timestamp
        self.validazione_timestamp(righe)

        #se righe è vuota alzo un'eccezione: o il file è vuoto o nessun dato è idoneo
        if not righe: 
            raise ExamException('File vuoto o nessun dato idoneo')

        # Quando ho processato tutte le righe, ritorno i valori
        return righe
    
    #creo una funzione che controlli che la serie temporale sia effettivamente ordinata in ordine crescente, se non lo è alzo un'eccezione
    def validazione_timestamp(self, righe):

        timestamp_precedente = -1 #-1 perchè so che qualsiasi numero inserito sarà > -1, non posso mettere ne None ne riga[0] altrimenti alza subito un'eccezione
        for riga in righe:
            if riga[0] < timestamp_precedente:
                raise ExamException("Attenzione! Timestamp fuori ordine (Potrebbero esserci anche dei duplicati!)")
            timestamp_precedente = riga[0]

        timestamp_precedente = -1 #-1 perchè so che qualsiasi numero inserito sarà > -1, non posso mettere ne None ne riga[0] altrimenti alza subito un'eccezione
        for riga in righe:
            if riga[0] == timestamp_precedente:
                raise ExamException("Attenzione! Timestamp duplicato")
            timestamp_precedente = riga[0]
   

#creo una funzione fuori dalla classe CSVTimeSeriesFile come da consegna
#che mi calcola le statistiche giornaliere
#[  [min_g1, max_g1, media1]     [min_g2, max_g2, media2]  ]
def daily_stats(time_series):

    #lista per salvarmi i risultati
    lista_giorno = [] 
    i = 0 #i si aggiorna ogni giorno

    #fino a che la lunghezza è < della lunghezza del file...
    while i < len(time_series):
        num_misurazioni = 0
        somma_misurazioni = 0
        # Salvo la prima temperatura come temperatura max e min del giorno
        min_giorno = time_series[i][1] #i = seleziono la sottolista, 1 = seleziono la temperatura 
        max_giorno = time_series[i][1]

        j = i #j si incrementa riga per rigaù

        #day_start_epoch = epoch-(epoch % 86400)
        day_start_epoch = time_series[i][0] - (time_series[i][0] % 86400) #primo momento del giorno 00.00 del giorno i
        day_start_epoch_1 = day_start_epoch #nel primo caso sono uguali --poi day_start_epoch_1 viene aggiornato--

        while (day_start_epoch == day_start_epoch_1):
            somma_misurazioni = somma_misurazioni + time_series[j][1]
            if time_series[j][1] < min_giorno:
                min_giorno = time_series[j][1]
            if time_series[j][1] > max_giorno:
                max_giorno = time_series[j][1]
            num_misurazioni = num_misurazioni + 1 #aggiorno il contatore
            j=j+1 #aggiorno j 
            if j<len(time_series): #controllo che j < lunghezza del file
                day_start_epoch_1 = time_series[j][0] - (time_series[j][0] % 86400) #calcolo il momento di inizio del giorno (giorno lettura j)
            else:
                break #esco del ciclo while annidato 
        media = somma_misurazioni/num_misurazioni
        lista_giorno.append([min_giorno, max_giorno, media])
        i = j #aggiorno i --> passo al giorno successivo

    return lista_giorno
        

time_series_file = CSVTimeSeriesFile(name="data.csv")
time_series = time_series_file.get_data()
statistiche = daily_stats(time_series)

print('Nome del file: "{}"'.format(time_series_file.name))

print('Dati contenuti nel file:')
print("[")
for dati in time_series_file.get_data():
    print(" {}".format(dati))
print("]")

print('Statistiche:')
print("[")
for statistica in statistiche:
    print(" {}".format(statistica))
print("]")