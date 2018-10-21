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
donnees_total_views=os.path.join(data_dir, "view_count.txt")
nb_vues=99

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

#recuperation du nombre de vues sur la chaine :
#import web page
s = urllib.urlopen(url)
page_web = s.read()

#accès au nombre actuel d'abonnés
donnees_page_web = json.loads(page_web.decode())
new_view_count = donnees_page_web["items"][0]["statistics"]["viewCount"]

print(new_view_count) #pour les tests
#ouverture du fichier avec l'ancien nombre d'abonnés
fichier_view_count = open(donnees_total_views, "r")
view_count = fichier_view_count.read()
print(view_count) #pour les tests
fichier_view_count.close()

#conversion des nombre d'abonnés en entiers pour pouvoir les comparer
new_view_count = int(new_view_count)
view_count = int(view_count)
#comparaison du nombre d'abonnés
diff = new_view_count-view_count
#condition : message telegram à envoyer selon la difference entre anciens abonnes et nouveaux abonnes
if diff > nb_vues:
	bot = telegram.Bot(api_tg_bot)
	bot.send_message(chat_id_tg, "Super ! {} nouvelles vues sur {}. Tu as maintenant {} vues".format(diff, channel, new_view_count))
else:
	pass
	
#s'il existe une différence entre anciens abonnés et nouveaux abonnés, conversion du nombre d'abonnés en caractères pour pouvoir envoyer new_sub_count dans le fichier
if diff > nb_vues:
	new_view_count = str(new_view_count)
	#mise à jour du fichier sub_count avec le nouveau nombre d'abonnés
	fichier_view_count = open(donnees_total_views, "w")
	fichier_view_count.write(new_view_count)
	fichier_view_count.close()
