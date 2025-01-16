import vk_api
import datetime
import time
import traceback
import settings
import random
ts = time.time()

vk_token = settings.vk_token
vk = vk_api.VkApi(token = vk_token)

EACH_NUM_POST = 20 
OUR_ID = vk.method('users.get')
OUR_ID = OUR_ID[0]['id']
with open('post_text.txt', mode = 'r', encoding ='utf-8') as f_t,open('post_text 1.txt', mode = 'r', encoding ='utf-8') as f_t1,open('post_text 2.txt', mode = 'r', encoding ='utf-8') as f_t2,open('post_text 3.txt', mode = 'r', encoding ='utf-8') as f_t3, open('post_att.txt', 'r') as f_a,  open('post_att 1.txt', 'r') as f_a1,  open('post_att 2.txt', 'r') as f_a2,  open('post_att 3.txt', 'r') as f_a3,open('groups.txt', 'r') as f_g:
	post_text = [f_t.read(), f_t1.read(), f_t2.read(), f_t3.read()]
	post_att = [f_a.read().replace('\n', ','), f_a1.read().replace('\n', ','), f_a2.read().replace('\n', ','), f_a3.read().replace('\n', ',')]
	groups = f_g.read().strip().split('\n')
while True:
	for group in groups:
		try:
			rs = vk.method('wall.get', {'count': EACH_NUM_POST, 'owner_id':group})
			flag = False
			for item in rs['items']:
				if item['from_id'] == OUR_ID:
					flag = True
					continue
			if not flag:
				dt = datetime.datetime.now()

				st = dt.strftime(dt.strftime("Day: %d/%m/%Y  time: %H:%M:%S"))
				print(f'In group {group} created post at {st}', vk.method('wall.post', {'message': post_text[random.randint(0, 3)], 'owner_id':group, 'attachment': post_att[random.randint(0, 3)]}))
				time.sleep (10)
		except Exception as e:
			erorr = str(traceback.format_exc())
			print(erorr)
	time.sleep (500)