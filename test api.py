from instagrapi import Client
import requests

cl = Client()
cl.login('jeugdhuis_de_muze', 'PYa9txU&LVRji^m@c2gEqceq@GQ$jDyV%Cf4UNRrJ5AKF!5o6#XzZo9jpWfQxYs^aJoUYUDq#x$Vj&WbdhAbbxE!X$nU7S9C*%eG5KP3KaqZVp$@UzQh8T^KoL*GwjKy')

# user_info = cl.user_info_by_username('jeugdhuis_de_muze')
# id = cl.user_id_from_username('jeugdhuis_de_muze')
# print(user_info)
7798204386
media = cl.user_medias('7798204386', 2)
for post in media:
    p = post.dict()
    url = p['thumbnail_url'].split(',')[0]
    img_data = requests.get(url).content
    with open(f"{p['id']}.jpg", 'wb') as handler:
        handler.write(img_data)