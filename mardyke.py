#
# This a really hacky implementation. Need to seperate it out into functions etc.
# Please do not judge me on this just a POC.
#

import requests
from datetime import datetime, timedelta

print("Booking Mardyke")

ACTIVITY_NAME = ['']
USERNAME = ''
PASSWORD = '!'

headers = {
    'authority': 'auth-plat.aws.glofox.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://app.glofox.com',
    'referer': 'https://app.glofox.com/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'x-glofox-branch-continent': 'EU',
    'x-glofox-branch-id': '5b6dd1a5e90c2d1f403fccb6',
    'x-glofox-branch-timezone': 'Europe/Dublin',
    'x-glofox-source': 'webportal',
    'x-is-lead-capture': 'false',
}

json_data = {
    'branch_id': '5b6dd1a5e90c2d1f403fccb6',
    'namespace': 'mardykearenaucc',
    'login': USERNAME,
    'password': PASSWORD,
}

response = requests.post('https://auth-plat.aws.glofox.com/login', headers=headers, json=json_data)

res = response.json()

if res['success'] == True:
  print("Logged in")
  token = res['token']

  headers = {
    'authority': 'api.glofox.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': 'Bearer ' + token,
    'origin': 'https://app.glofox.com',
    'referer': 'https://app.glofox.com/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'x-glofox-branch-continent': 'EU',
    'x-glofox-branch-id': '5b6dd1a5e90c2d1f403fccb6',
    'x-glofox-branch-timezone': 'Europe/Dublin',
    'x-glofox-source': 'webportal',
    'x-is-lead-capture': 'false',
  }

  timenow = str(int(datetime.now().timestamp()))
  time48hrs = str(int((datetime.now() + timedelta(hours=48)).timestamp()))
  
  page = 1
  hasmore = True

  while hasmore == True:
    response = requests.get(
      'https://api.glofox.com/2.0/events?end=' + time48hrs + '&include=trainers,facility,program,users_booked&page=' + str(page) + '&private=false&sort_by=time_start&start=' + timenow,
      headers=headers,
    )

    res = response.json()

    page = page + 1
    hasmore = res['has_more']

    for item in res['data']:

      if item['name'] in ACTIVITY_NAME:

        print('Booking:')
        print(item['name'])
        print(item['_id'])

        headers = {
            'authority': 'api.glofox.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'authorization': 'Bearer ' + token,
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://app.glofox.com',
            'referer': 'https://app.glofox.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'x-glofox-branch-continent': 'EU',
            'x-glofox-branch-id': '5b6dd1a5e90c2d1f403fccb6',
            'x-glofox-branch-timezone': 'Europe/Dublin',
            'x-glofox-source': 'webportal',
            'x-is-lead-capture': 'false',
        }
        
        json_data = {
            'pay_gym': False,
            'guest_bookings': 0,
            'model': 'event',
            'model_id': item['_id'],
        }
        
        response = requests.post('https://api.glofox.com/2.0/bookings', headers=headers, json=json_data)
        print('Success:')
        print(response.json()['success'])
