# -*- coding: utf-8 -*-

import requests

from encrypt import encrypted_request
from constants import headers
from constants import song_download_url
from constants import get_song_url
from constants import get_album_url
from constants import get_artist_url
from constants import get_playlist_url
from constants import get_song_id_url
import urllib3
import json


class CloudApi(object):

    def __init__(self, timeout=30):
        super().__init__()
        self.session = requests.session()
        self.session.headers.update(headers)
        self.timeout = timeout

    def get_request(self, url):
        response = self.session.get(url, timeout=self.timeout)
        result = response.json()
        if result['code'] != 200:
            print('Return {} when try to get {}'.format(result, url))
        else:
            return result

    def post_request(self, url, params):

        data = encrypted_request(params)
        response = self.session.post(url, data=data, timeout=self.timeout)
        result = response.json()
        if result['code'] != 200:
            print('Return {} when try to post {} => {}'.format(result, params, url))
        else:
            return result

    def post_request_ex(self, url, params):

        # data = encrypted_request(params)
        response = self.session.post(url, data=params, timeout=self.timeout)
        print(response)
        result = response.json()
        if result['code'] != 200:
            print('Return {} when try to post {} => {}'.format(result, params, url))
        else:
            return result



    def get_song_id_base(self, songname, singger=""):
        """
        Get song id by song name and singger
        :param songname:
        :param singger:
        :return:
        """
        # http = urllib3.PoolManager
        # http.request("GET",get_song_id_url(key_word))
        url = get_song_id_url()
        params = {'s': songname, 'offset': "0", 'type': "1", 'limit': "1"}
        result = self.post_request_ex(url, params)
        print(result)
        count=result['result']['songCount']
        id=""
        for i in range(int(count/10)+1):
            params['offset'] = i*10
            params['limit'] = 10
            result = self.post_request_ex(url,params)

            for x in range(10):
                try:
                    print("{}/{}=>{}".format(i,count,result))
                    if result['result']:
                        # songnameData=result['result']['songs'][0]['name']
                        singgername = result['result']['songs'][0]['artists'][0]['name']
                        id=result['result']['songs'][0]['id']
                        # if (not singger ) or ((singgername.strip().index(singger.strip())>-1) or (songnameData.index(singger)>-1)):
                        if (not singger) or (singgername.strip() == (singger.strip())):
                            return id
                except:
                    ""




    def get_song_id(self, songname, singger):
        """
        Get song id by song name and singger
        :param songname:
        :param singger:
        :return:
        """
        ida = self.get_song_id_base(songname, singger)
        if not ida:
            ida = self.get_song_id_base(songname+" "+singger)
        return ida

    def get_song(self, song_id):
        """
        Get song info by song id
        :param song_id:
        :return:
        """
        url = get_song_url(song_id)
        result = self.get_request(url)

        return result['songs'][0]

    def get_album_songs(self, album_id):
        """
        Get all album songs info by album id
        :param album_id:
        :return:
        """
        url = get_album_url(album_id)
        result = self.get_request(url)

        return result['album']['songs']

    def get_song_url(self, song_id, bit_rate=320000):
        """Get a song's download url.
        :params song_id: song id<int>.
        :params bit_rate: {'MD 128k': 128000, 'HD 320k': 320000}
        :return:
        """
        url = song_download_url
        csrf = ''
        params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        result = self.post_request(url, params)
        song_url = result['data'][0]['url']
        return song_url

    def get_hot_songs(self, artist_id):
        """
        Get a artist 50 hot songs
        :param artist_id:
        :return:
        """
        url = get_artist_url(artist_id)
        result = self.get_request(url)
        return result['hotSongs']

    def get_playlist_songs(self, playlist_id):
        """
        Get a public playlist all songs
        :param playlist_id:
        :return:
        """
        url = get_playlist_url(playlist_id)
        result = self.get_request(url)
        return result['result']['tracks'], result['result']['name']



