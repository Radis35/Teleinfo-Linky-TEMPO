import serial
import pymysql
import time
print("debut programme")
# Configuration du port série
SERIAL_PORT = '/dev/ttyAMA0'
BAUD_RATE = 1200
START_FRAME = b'\x02'  # STX, Start of Text
STOP_FRAME = b'\x03'   # ETX, End of Text
temps=0

# Configuration de la connexion à la base de données MariaDB
DB_HOST = 'localhost'
DB_USER = 'user'  # Remplacez par votre nom d'utilisateur
DB_PASSWORD = 'password!'  # Remplacez par votre mot de passe
DB_NAME = 'dbname'
print("DB_configuree")

# Liste pour stocker les lignes d'une trame complète
trame_complete = []

try:
    # Configuration de la connexion série
    ser= serial.Serial(port=SERIAL_PORT,
                           baudrate=BAUD_RATE,
                           parity=serial.PARITY_EVEN,
                           stopbits=serial.STOPBITS_ONE,
                           bytesize=serial.SEVENBITS,
                           timeout=1)
    line = ser.readline()
    print(ser)
    print(line)
    print("fin init")


    while START_FRAME not in line:  # Recherche du caractère de début de trame, c'est-à-dire STX 0x0
        line = ser.readline()
        print("debut trame trouvee")
        t1=time.time()
      # Lire les données depuis le port série
    while True:
        try:
            # Lecture de la première ligne de la première trame
            line = ser.readline()

            # Décodage ASCII et nettoyage du retour à la ligne
            line_str = line.decode('ascii').rstrip()

            #line = ser.readline().decode('ascii', errors='replace').strip()
            #print("Ligne lue depuis le port série:", line_str)
            
            # Ajouter la ligne décodée à la liste de la trame complète
            trame_complete.append(line_str)

  	    # Si caractère de fin de trame dans la ligne, on écrit les données dans InfluxDB
            if STOP_FRAME in line:
                print("fin trame")

                # Afficher la trame complète
                #print("Trame complète:", trame_complete)
                # Afficher chaque ligne de la trame complète
                for ligne in trame_complete:
                    print(ligne)

                # Parcourir chaque ligne de la trame complète
                for ligne in trame_complete:
                    if ligne.startswith('IINST'):
                        iinst_value = int(ligne.split(' ')[1])
                        print('IINST:', iinst_value)
                    elif ligne.startswith('PAPP'):
                        papp_value = int(ligne.split(' ')[1])
                        print('PAPP:', papp_value)


                # Connexion à la base de données
                conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
                cursor = conn.cursor()
                print("connexion DB reussi")
                # Insertion des valeurs dans la table "mesure"
                if iinst_value is not None and papp_value is not None:
                    sql_insert = "INSERT INTO mesure (intensite_instantanee, puissance_apparente) VALUES (%s, %s)"
                    cursor.execute(sql_insert, (iinst_value, papp_value))
                    conn.commit()
                    print("Valeurs insérées avec succès dans la base de données.")

                # Fermeture de la connexion à la base de données 
                cursor.close()
                conn.close()


                # Réinitialiser la liste pour stocker une nouvelle trame complète
                trame_complete = []
                temps=0
                while (temps<5):
                    t2=time.time()
                    temps=t2-t1
                    time.sleep(1)
                    print(temps)
                ser.flushInput()
                line=ser.readline()
                while START_FRAME not in line:  # Recherche du caractère de début de trame, c'est-à-dire STX 0x0
                    line = ser.readline()
                    print("debut trame trouvee")
                    t1=time.time()

        except UnicodeDecodeError as e:
            print("Erreur de décodage : ", str(e))

    
except KeyboardInterrupt:
    # En cas d'interruption par l'utilisateur (Ctrl+C), fermer la connexion série
    ser.close()
