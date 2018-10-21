# coding: utf-8

"""
helped me :
https://www.linkedin.com/pulse/telegram-bots-beginners-marco-frau : step 5 to retrieve chat_id
https://github.com/python-telegram-bot/python-telegram-bot : pip install pour utiliser telegram
"""

import os
import json
import urllib
import telegram
import sys
from time import sleep

data_dir="/home/louvine/dev/cm_counts/"
donnees_file=os.path.join(data_dir, "donnees.json")
donnees_total_views=os.path.join(data_dir, "view_count.txt")
donnees_video_views=os.path.join(data_dir, "video_views.json")

#variable : différence que je veux entre l'ancien nombre de vues et le nouveau nombre de vues pour l'envoie du message, pour l'instant >9
diff_min = 9
#nombre de secondes entre deux envois telegram pour eviter d'activer l'anti spam telegram
sleeptime = 2
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
url_videos = donnees_json["url_videos"]
url_video_views = donnees_json["url_video_views"]

#recuperation de la liste des videos par id :
#import web page
s = urllib.urlopen(url_videos)
page_web = s.read()
donnees_page_web = json.loads(page_web.decode("utf-8"))

#ouverture du fichier contenant le dictionnaire avec les video_id en clé et le nombre de vues de la video en valeur
fichier_video_views = open(donnees_video_views, "r")
video_views_count = fichier_video_views.read()
video_views_count = json.loads(video_views_count.decode())

#boucle
for item in donnees_page_web["items"]:
	#pour corriger l'erreur des playlist, on conditionne la recherche du nombre de vues ) la présence de videoId dans chaque item car sinon c'est une playlist sans nombre de vues
	if "videoId" in item["id"]:
		#récupération de l'id de la video
		video_id = item["id"]["videoId"]
		if video_id not in video_views_count:
			video_views_count[video_id]=0

		#url à aller regarder en insérant l'id de la video
		url_video_views="https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id="+video_id+"&key="+api_key
		so = urllib.urlopen(url_video_views)
		pweb = so.read()
		donnees_pweb = json.loads(pweb.decode("utf-8"))
		title = donnees_pweb["items"][0]["snippet"]["title"].encode("utf-8")
		if "maxres" in donnees_pweb["items"][0]["snippet"]["thumbnails"]:
			keyres="maxres"
		else:
			keyres="high"
		link_img = donnees_pweb["items"][0]["snippet"]["thumbnails"][keyres]["url"]
		#dans la variable new_video_views_count on met la valeur trouvée en déchiffrant la page
		new_video_views_count = int(donnees_pweb["items"][0]["statistics"]["viewCount"])
		 #si l'ancien dictionnaire  ne contient pas une clé[videoId], alors on la crée
                #if video_id not in video_views_count:
                #        video_views_count[video_id]=new_video_views_count
		#pour le test
		print(video_id)
		#dans vvcount on met ce qu'il y a dans le fichier : la valeur de la clé[video_id]
		vvcount = video_views_count[video_id]
		#pour les tests
		print(video_views_count[video_id])
		print(new_video_views_count)
		#si l'ancien nombre de vues est différent du nouveau nombre de vues de >10, alors on écrit dans le dico la nouvelle valeur
		diff = new_video_views_count - video_views_count[video_id]
		print(diff)
		if diff>diff_min:
			bot = telegram.Bot(api_tg_bot)
			bot.send_message(chat_id_tg, "Super ! {} nouvelles vues sur {}. Tu as maintenant {} vues\n {}".format(diff, title, new_video_views_count, link_img))
			sleep(sleeptime)
			video_views_count[video_id]=new_video_views_count

#json.dumps transforme le dictionnaire en chaine de caractère, json.loads fait le contraire
dico = video_views_count
jsonarray = json.dumps(dico)

fichier_dico = open(donnees_video_views, "w")
fichier_dico.write(jsonarray)
fichier_dico.close()

