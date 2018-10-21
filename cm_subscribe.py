# coding: utf-8

"""
helped me :
https://www.youtube.com/watch?v=yZLFfqqnO6c : to get subscriberCount
https://www.linkedin.com/pulse/telegram-bots-beginners-marco-frau : step 5 to retrieve chat_id
https://github.com/python-telegram-bot/python-telegram-bot : pip install pour utiliser telegram
"""

import os
import json
import urllib
import telegram

data_dir="/home/louvine/dev/cm_counts/"
donnees_file=os.path.join(data_dir, "donnees.json")
donnees_sub_count=os.path.join(data_dir, "sub_count.txt")
#importation des données depuis un fichier json :
#ouverture du fichier pour récupérer la chaine de caractère
fichier_donnees = open(donnees_file, "r")
donnees = fichier_donnees.read()
#lecture de la chaine de caractère 
donnees_json = json.loads(donnees)
#récupération des variables
channel_id = donnees_json["id_chaine"]
channel = donnees_json["nom_chaine"].encode("utf-8") #.encode car accent dans le nom de la chaine
api_key = donnees_json["cle_api"]
url = donnees_json["url"]
api_tg_bot = donnees_json["api_tg_bot"]
chat_id_tg = donnees_json["chat_id_louvine_tg"]

#recuperation du nombre d'abonnés :
#import web page
s = urllib.urlopen(url)
page_web = s.read()

#accès au nombre actuel d'abonnés
donnees_page_web = json.loads(page_web.decode())
new_sub_count = donnees_page_web["items"][0]["statistics"]["subscriberCount"]

print(new_sub_count) #pour les tests
#ouverture du fichier avec l'ancien nombre d'abonnés
fichier_sub_count = open(donnees_sub_count, "r")
sub_count = fichier_sub_count.read()
print(sub_count) #pour les tests
fichier_sub_count.close()

#conversion des nombre d'abonnés en entiers pour pouvoir les comparer
new_sub_count = int(new_sub_count)
sub_count = int(sub_count)
#comparaison du nombre d'abonnés
diff = new_sub_count-sub_count
#condition : message telegram à envoyer selon la difference entre anciens abonnes et nouveaux abonnes
if diff > 0 and diff < 2:
	bot = telegram.Bot(api_tg_bot)
	bot.send_message(chat_id_tg, "Super ! 1 nouvel abonné sur {}. Tu as maintenant {} abonnés".format(channel, new_sub_count))
elif diff >=2:
	bot = telegram.Bot(api_tg_bot)
	bot.send_message(chat_id_tg, "Super !!! {} nouveaux abonnes sur {}. Tu as maintenant {} abonnés".format(diff, channel, new_sub_count))
elif diff ==-1:
	bot = telegram.Bot(api_tg_bot)
	bot.send_message(chat_id_tg, "tu perds 1 abonné sur {}. Tu as maintenant {} abonnés".format(channel, new_sub_count))
elif diff <-1:
	bot = telegram.Bot(api_tg_bot)
	bot.send_message(chat_id_tg, "Ho non ! {} abonnés en moins sur {}. Tu as maintenant {} abonnés".format(diff, channel, new_sub_count))
else:
	pass
	
#s'il existe une différence entre anciens abonnés et nouveaux abonnés, conversion du nombre d'abonnés en caractères pour pouvoir envoyer new_sub_count dans le fichier
if diff != 0:
	new_sub_count = str(new_sub_count)
	#mise à jour du fichier sub_count avec le nouveau nombre d'abonnés
	fichier_sub_count = open(donnees_sub_count, "w")
	fichier_sub_count.write(new_sub_count)
	fichier_sub_count.close()
