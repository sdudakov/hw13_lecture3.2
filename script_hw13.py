from pprint import pprint
import vk
from urllib.parse import urlencode, urlparse
import requests


AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
APP_ID = 5977773 # Your app_id here

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends,status,video',
    'v': VERSION,
}
#print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

token_url = 'https://oauth.vk.com/blank.html#access_token=c68700af6cdbb86e159ec433de4982026de329b8c5d41dd48e44710ee2fbd534804aefc6484ae2968250e&expires_in=86400&user_id=423358763'

o = urlparse(token_url)
fragments = dict((i.split('=') for i in o.fragment.split('&')))
access_token = fragments['access_token']

params = {'access_token': access_token,
          'v': VERSION,
          }

#функция возвращает список участников группы
def group_members(group_id):
    params['group_id'] = group_id
    response = requests.get('https://api.vk.com/method/groups.getMembers', params)
    group_members = response.json()['response']['items']
    return group_members

#пересечение (общих друзей) между полученными пользователями.
def ferends_crossing(group_members):
    frends = set() #создаю пустое множество
    for user_id in group_members:
        params['user_id'] = user_id
        response = requests.get('https://api.vk.com/method/users.get', params) # получаю информацию о каждом пользователе группы
        if not 'deactivated' in response.json()['response'][0]: # проверяю не заблокирован ли пользователь
            params['user_id'] = response.json()['response'][0]['id']
            frends_list = requests.get('https://api.vk.com/method/friends.get', params) # получаю список друзей пользователя
            for item in frends_list.json()['response']['items']:
                frends.add(item) # добавляю id друзей во множество - там будут только уникальные записи
    return frends

# 4233581 случайная группа с небольшим количеством участников
print(ferends_crossing(group_members(4233581)))

