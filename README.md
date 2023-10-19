# Teleinfo-Linky-TEMPO
Un petit tuto et code python pour voir les données de la téléinformation transmise par le linky au traver d'un raspberry Pi Zero


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
