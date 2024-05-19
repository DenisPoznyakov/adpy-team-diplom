# это пробный образец кода, что бы доставать ссылки, лайки, айди и прочую инфу из json файлов фотографий

import json
from pprint import pprint
photos_likes_profile = []

with open ('return photos info example.json', 'r') as file:
    photo_info = json.load(file)

    for photo in photo_info['response']['items']:
        likes = photo['likes']['count']
        photo_id = photo['id']

        for i in photo['sizes']:
            link_list = []
            link_list.append(i['url'])
            link = link_list[-1] #костыли с получением ссылки на фото

        photos_likes_profile.append([likes, photo_id, link])

        # попытка получать ссылку на фото с максимальным разрешением
        # size_max = 0
        # for i in photo['sizes']:
        #     if i['height'] >= size_max:
        #         size_max = i['height']
        #         # print(size_max)
        #         if photo['likes']['count'] not in max_size_photo.keys():
        #             max_size_photo[photo['likes']['count']] = i['url']
        #         else:
        #             max_size_photo[f"{photo['likes']['count']} + {photo['date']}"] = i['url']

photos_likes_profile.sort()
photos_likes_profile_best = [photos_likes_profile[-1], photos_likes_profile[-2], photos_likes_profile[-3]]
pprint(photos_likes_profile_best)
