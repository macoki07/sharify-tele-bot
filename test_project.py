from project import handle_response
from spotify_api import get_album_id, get_artist_id, get_song_id, get_token

def main():
    test_handle_response()
    test_get_album_id()
    test_get_artist_id()
    test_get_song_id()

def test_handle_response():
    assert handle_response('hello') == 'Type /help for the usage of Sharify!'
    assert handle_response('-album lion') == 'https://open.spotify.com/album/6PwjeKXh33Xze41oTPhJUh'
    assert handle_response('-song roar') == 'https://open.spotify.com/track/27tNWlhdAryQY04Gb2ZhUI'
    assert handle_response('-artist ed sheeran') == 'https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V'

def test_get_album_id():
    token = get_token()
    assert get_album_id(token, 'lion') == '6PwjeKXh33Xze41oTPhJUh'

def test_get_artist_id():
    token = get_token()
    assert get_artist_id(token, 'ed') == '6eUKZXaKkcviH0Ku9w2n3V'

def test_get_song_id():
    token = get_token()
    assert get_song_id(token, 'roar') == '27tNWlhdAryQY04Gb2ZhUI'

if __name__ == "__main__":
    main()