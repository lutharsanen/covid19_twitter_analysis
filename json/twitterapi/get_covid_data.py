import requests
import base64
import json
import time

base = 'https://api.twitter.com/1.1/tweets/search/'
#Define your keys from the developer portal
client_key = ''
client_secret = ''
#Reformat the keys and encode them
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

# Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')

# Do first request manually and paste next_page here
next_page = ''


def auth():
    auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key)
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post('https://api.twitter.com/oauth2/token', headers=auth_headers, data=auth_data)
    token = auth_resp.json()['access_token']

    session = requests.Session()
    session.headers = {'Authorization': 'Bearer ' + token}
    return session


def get30daysIT(session):
    global next_page

    res = session.post('https://api.twitter.com/1.1/tweets/search/30day/dev.json', json={
        "query" : "place_country:IT (#COVID19 OR #COVID-19 OR #covid_19 OR #covid OR #corona OR #coronavirus)",
        "fromDate":"202003120000", 
        "toDate":"202004110000",
        "next": next_page
    })

    json_res = res.json()
    try:
        next_page = json_res['next']

    except:
        next_page = None

    print('next_page ', next_page)

    return json_res


def get30daysNY(session):
    global next_page

    res = session.post('https://api.twitter.com/1.1/tweets/search/30day/dev.json', json={
        "query" : "place:NY (#COVID19 OR #COVID-19 OR #covid_19 OR #covid OR #corona OR #coronavirus)",
        "fromDate":"202003120000", 
        "toDate":"202004110000",
        "next": next_page
    })

    json_res = res.json()
    try:
        next_page = json_res['next']

    except:
        next_page = None

    print('next_page ', next_page)

    return json_res


if __name__ == "__main__":
    session = auth()

    i = 1

    while True:
        # avoid rate limits
        time.sleep(5)
        res = get30daysNY(session)

        with open('ny-' + str(i) + '.json', 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

        i += 1

        if next_page == None:
            break
