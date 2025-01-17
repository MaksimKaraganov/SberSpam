import os
import vk_api
import datetime
import time
import traceback
import settings
import random
from requests import Session
ts = time.time()
IMAGE_FOLDER = 'images'

class Account:
	def __init__(self, session, proxies, token):
		self.session = session
		self.session.proxies = proxies
		self.token = token
		self.vk = vk_api.VkApi(token=token, session=session)
		self.OUR_ID = self.vk.method('users.get')
		self.OUR_ID = self.OUR_ID[0]['id']
		self.image_attachments = upload_images_to_vk(self, folder_path=IMAGE_FOLDER)


EACH_NUM_POST = 20 

def upload_images_to_vk(user: Account, folder_path):
	attachments = []
	try:
		for filename in os.listdir(folder_path):
			if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
				image_path = os.path.join(folder_path, filename)

				# Получение URL для загрузки фото
				upload_url = user.vk.method('photos.getWallUploadServer')['upload_url']

				# Загрузка файла
				with open(image_path, 'rb') as image_file:
					response = user.session.post(upload_url, files={'photo': image_file}).json()

				# Сохранение загруженного фото
				saved_photo = user.vk.method('photos.saveWallPhoto', {
					'photo': response['photo'],
					'server': response['server'],
					'hash': response['hash']
				})[0]

				# Добавление attachment строки
				attachments.append(f"photo{saved_photo['owner_id']}_{saved_photo['id']}")
	except Exception as e:
		print(f"Error uploading images: {e}")
	return attachments

credentials = [
	('vk1.a.PURWXzT62S9KhdA465_cv9DvuoQUO37v668E7DYnm2dCeVli9rMKxVxoYaW5tyD4HTmR6WdD3yM-oC3A_QkSvwHJvHiRwIPQExpJHUZa41-Aq2a4EmuwYy74A1xVcOBPiCfcplaem2E9SlSJdUL9xMQOcrZ8lZxsrCqVoxsqhCr9jsr1_ovM5sH4-jX2CBMATGCmVqaM41Z6Zxfq7MUoZw','socks5://4eigmwpxxk-corp.mobile.res-country-RU-state-491684-city-491687-hold-session-session-6789736828c5c:Rzw43zL9SP460cqQ@138.201.49.224:9999'),
	('vk1.a.GnoFyUNqDETH3EPJLMoExN9iEfgRoTRGAESgYO7bqKolUfET26qmOWQSfaNRUmjlgMoCWaASg7GLSmHyo1MIBSDeH328ifIuhtSpbNMes-QbC5TCfNDNeQOG4-tv1jG6-pKnbz_70IHOFdJeYPImVvCnt-HAKcS1lxw6rs4QI86O1T4zY0GOS1exrVXRt8t9-cOvX_bartdlY8k01C_3bQ','socks5://4eigmwpxxk-corp.mobile.res-country-RU-state-524894-city-524901-hold-session-session-678ac46929907:Rzw43zL9SP460cqQ@88.99.166.254:9999'),
]


users = [ Account(Session(), proxies=credential[1], token=credential[0])
	  for i, credential in enumerate(credentials)
	]
# Загружаем изображения из папки images
with open('post_text.txt', mode = 'r', encoding ='utf-8') as f_t,open('post_text 1.txt', mode = 'r', encoding ='utf-8') as f_t1,open('post_text 2.txt', mode = 'r', encoding ='utf-8') as f_t2,open('post_text 3.txt', mode = 'r', encoding ='utf-8') as f_t3,open('groups.txt', 'r') as f_g:
	post_text = [f_t.read(), f_t1.read(), f_t2.read(), f_t3.read()]
	groups = f_g.read().strip().split('\n')
last_group = groups[0]
user: Account = users[random.randint(0,len(users)-1)]
while True:
	i = 0
	for group in groups[groups.index(last_group):]:
		try:
			last_group = group
			rs = user.vk.method('wall.get', {'count': EACH_NUM_POST, 'owner_id':group})
			flag = False
			for item in rs['items']:
				for our_user in users:
					if item['from_id'] == our_user.OUR_ID:
						flag = True
						continue
			if not flag:
				dt = datetime.datetime.now()

				st = dt.strftime(dt.strftime("Day: %d/%m/%Y  time: %H:%M:%S"))
				print(f'In group {group} created post at {st}', user.vk.method('wall.post', {'message': post_text[random.randint(0, len(post_text)-1)], 'owner_id':group, 'attachment': user.image_attachments[random.randint(0, len([user.image_attachments])-1)]}))
				time.sleep (random.randint(7,23))
				if i % 6 == 0:
					time.sleep(random.randint(30,40))
				if i>12:
					print('im finished')
					new_user = 	users[(users.index(user)+1)%len(users)]
					user = new_user
					i = 0
					break
		except Exception as e:
			err = str(traceback.format_exc())
			print(err)
	last_group = groups[0]