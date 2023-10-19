# Teleinfo-Linky-TEMPO
Un petit tuto et code python pour voir les données de la téléinformation transmise par le linky au traver d'un raspberry Pi Zero


Prérequis matériel:
- Un compteur linky avec le bornier TIC accessible
- Un raspberry pi zero W
- Un module téléinfo (optocoupleur) pour protéger votre linky : https://www.tindie.com/products/hallard/pitinfo/

Prérequis logiciel : 
- Grafana pour archi ARMv6 : https://grafana.com/grafana/download/10.1.2?platform=arm
- Serveur MariaDB :
          - Installer le serveur : https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-               ubuntu-20-04-quickstart-fr
          - Paramétrer les utilisateurs : https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-           on-ubuntu-20-04-quickstart-fr

Prérequis Pyhton :
Sur Raspberry Pi OS vous avez déjà la dernière version de Python3. Mais vous allez devoir installer plusieurs bilbliothèques :
- pyserial : sudo pip install pyserial
