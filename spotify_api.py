from dotenv import dotenv_values
import base64
from requests import get, post
import json

config = dotenv_values('.env')

id = config['SPOTIFY_ID']
secret = config['SPOTIFY_SECRET']

def main():
    print('Empty by design')
    
def get_token():
    auth_str = id + ':' + secret
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

def get_artist_id(token, name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={name}&type=artist&limit=1'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items'][0]['id']

    if len(json_result) == 0:
        print(f'No artist found with the name {name}')
        return None
    
    # print(json_result)
    return json_result

def get_artist_link(token, id):
    url = f'https://api.spotify.com/v1/artists/{id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['external_urls']['spotify']
    return json_result

def get_song_id(token, name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={name}&type=track&limit=1'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['tracks']['items'][0]['id']

    if len(json_result) == 0:
        print(f'No song found with the name {name}')
        return None
    
    # print(json_result)
    return json_result

def get_song_link(token, id):
    url = f'https://api.spotify.com/v1/tracks/{id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['external_urls']['spotify']
    return json_result

def get_album_id(token, name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={name}&type=album&limit=1'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['albums']['items'][0]['id']

    if len(json_result) == 0:
        print(f'No album found with the name {name}')
        return None
    
    # print(json_result)
    return json_result

def get_album_link(token, id):
    url = f'https://api.spotify.com/v1/albums/{id}'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['external_urls']['spotify']
    return json_result

token = get_token()
# id = get_artist_id(token, 'acdc')
# print(get_artist_link(token, id))
# id = get_track_id(token,'roar')
# print(get_track_link(token,id))
# id = get_album_id(token,'lion')
# print(get_album_link(token,id))

if __name__ == "__main__":
    main()