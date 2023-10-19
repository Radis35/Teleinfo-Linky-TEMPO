# Teleinfo-Linky-TEMPO
Un petit tuto et code python pour voir les données de la téléinformation transmises par le linky au traver d'un raspberry Pi Zero


## Prérequis matériel:
- Un compteur linky avec le bornier TIC accessible
- Un raspberry pi zero W
- Un [module téléinfo](https://www.tindie.com/products/hallard/pitinfo/) (optocoupleur) pour protéger votre linky 

## Prérequis configuration matériel:
Dans notre programme nous allons récupérer les données du Linky au travers du port série UART PL011 `dev/ttyAMA0` utilisé par défaut par le BT. Pour cela il faudra faire les modifications suivantes : 

Activer l'UART          
Désactiver le Bluetooth          
Désactiver le port console sur l'interface série          
Ajouter à la fin de `/boot/config.txt`          

```
#Enable UART
enable_uart=1

#Disable Bluetooth
dtoverlay=disable-bt
```

Editer `/boot/cmdline.txt` et retirer `console=serial0,115200`

Désactiver les services Bluetooth 
```
sudo systemctl disable hciuart 
sudo systemctl disable bluetooth.service
```
Redémarrez.

### Tester le port série

Installer et lancer Picocom :
```
sudo apt-get install picocom
```
```
picocom -b 1200 -d 7 -f n /dev/ttyAMA0
```

Vous devriez voir apparaitre les trames sous ce format : 
```
ADCO 031562151396 A
OPTARIF BBR( S
ISOUSC 60CJB 052272737 @
BBRHPJB 049771526 S
BBRHCJW 000000000 2
BBRHPJW 000000000 ?
BBRHCJR 000000000 -
BBRHPJR 000000000 :
PTEC HPJB P
DEMAIN ---- "
IINST 002 Y
IMAX 090 H
PAPP 00520 (
HHPHC A ,
MOTDETAT
```

Pour quitter : Crtl+A puis Ctrl+X

## Prérequis logiciel : 
- [Grafana pour archi ARMv6](https://grafana.com/grafana/download/10.1.2?platform=arm)
- Serveur MariaDB :          
[Installer le serveur](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04-quickstart-fr)
[Paramétrer les utilisateurs](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04-quickstart-fr)

## Prérequis Pyhton :
Sur Raspberry Pi OS vous avez déjà la dernière version de Python3. Mais vous allez devoir installer plusieurs bilbliothèques (pyserial et pymsql):
```
sudo pip install pyserial
sudo pip install pymysql
```
Il se peut que le système vous demande de vous placer dans un environnement virtuel (que je n'ai pas fait) et vous donne les commandes pour passer outre et installer ceci dans l'environnement global.

## Prérequis base de donnée :

Maintenant que les prérequis sont en place il faut créer une base de donnée et un utilisateur :
```
sudo mysql
```

```
mysql> CREATE DATABASE linky;
mysql> CREATE USER 'user'@'localhost' IDENTIFIED BY 'motdepasse';
mysql> GRANT ALL PRIVILEGES ON linky.* TO 'user'@'localhost';
mysql> FLUSH PRIVILEGES;
```
```
USE linky;
```
Création d'une table 'mesure' et des colonnes puissance_apparente, intensite_instantanee et horodatage
```
CREATE TABLE mesure (
    puissance_apparente INT,
    intensite_instantanee INT,
    horodatage TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## configuration du programme :

Vous devez maintenant configuer les paramètres de votre base données dans le programme

```
# Configuration de la connexion à la base de données MariaDB
DB_HOST = '127.0.0.1'
DB_USER = 'user'  # Remplacez par votre nom d'utilisateur
DB_PASSWORD = 'password!'  # Remplacez par votre mot de passe
DB_NAME = 'linky'
```
## Test du programme :

Et voilà vous êtes prêt pour tester le programme, vous pouvez le lancer avec la commande : 
```
python3 linky.py
```
Vous devriez voir apparaitre les étapes du programme et en arrière plan la base de donnée commence à se charger.

Pour vérifier vous pouvez lancer votre base de donnée dans un autre shell :

```
sudo mysql
```

```
USE linky;
```
```
select * from mesure;
```

Vous devriez voir apparaitre ceci : 
```
+---------------------+-----------------------+---------------------+
| puissance_apparente | intensite_instantee   |     horodatage      |
+---------------------+-----------------------+---------------------+
|                 520 |                     2 | 2023-10-19 13:31:56 |
|                 530 |                     2 | 2023-10-19 13:32:03 |
|                 530 |                     2 | 2023-10-19 13:32:11 |
|                 530 |                     2 | 2023-10-19 13:32:18 |
|                 420 |                     2 | 2023-10-19 13:32:25 |
|                 420 |                     2 | 2023-10-19 13:32:33 |
|                 430 |                     2 | 2023-10-19 13:32:40 |
|                 430 |                     2 | 2023-10-19 13:32:47 |
|                 430 |                     2 | 2023-10-19 13:32:55 |
|                 430 |                     2 | 2023-10-19 13:33:02 |
|                 430 |                     2 | 2023-10-19 13:33:10 |
|                 430 |                     2 | 2023-10-19 13:33:17 |
+---------------------+-----------------------+---------------------+
```
##Affichage dans Grafana

Grafana est accessible depuis un navigateur web à l'adresse 
```
adresse_ip_du_rasp:3000
```

je vous met un fichier de conf. JSON dans les fichiers pour avoir ce type de graphique (attention à la zone horaire, UTC ici)

![Capture d'écran 2023-10-19 161803.png]
