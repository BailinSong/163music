# -*- coding: utf-8 -*-
import argparse
import os

from urllib.parse import urlparse, parse_qs
import config
from api import CloudApi
from downloader import download_song_by_id
from downloader import download_song_by_song
from downloader import format_string
from downloader import download_song_by_key_word
# load the config first
config.load_config()
api = CloudApi()


def download_hot_songs(artist_id):
    songs = api.get_hot_songs(artist_id)
    folder_name = format_string(songs[0]['artists'][0]['name']) + ' - hot50'
    folder_path = os.path.join(config.DOWNLOAD_DIR, folder_name)
    download_count = config.DOWNLOAD_HOT_MAX if (0 < config.DOWNLOAD_HOT_MAX < 50) else config.DOWNLOAD_HOT_MAX_DEFAULT
    for i, song in zip(range(download_count), songs):
        print('{}: {}'.format(i + 1, song['name']))
        download_song_by_song(song, folder_path, False)


def download_album_songs(album_id):
    songs = api.get_album_songs(album_id)
    folder_name = format_string(songs[0]['album']['name']) + ' - album'
    folder_path = os.path.join(config.DOWNLOAD_DIR, folder_name)
    for i, song in enumerate(songs):
        print('{}: {}'.format(i + 1, song['name']))
        download_song_by_song(song, folder_path, False)


def download_playlist_songs(playlist_id):
    songs, playlist_name = api.get_playlist_songs(playlist_id)
    folder_name = format_string(playlist_name) + ' - playlist'
    folder_path = os.path.join(config.DOWNLOAD_DIR, folder_name)
    for i, song in enumerate(songs):
        print('{}: {}'.format(i + 1, song['name']))
        download_song_by_song(song, folder_path, False)


def get_parse_id(song_id):
    # Parse the url
    if song_id.startswith('http'):
        # Not allow fragments, we just need to parse the query string
        return parse_qs(urlparse(song_id, allow_fragments=False).query)['id'][0]
    return song_id


def main():
    parser = argparse.ArgumentParser(description='Welcome to netease cloud music downloader!')
    parser.add_argument('-s', metavar='song_id', dest='song_id',
                        help='Download a song by song_id')
    parser.add_argument('-ss', metavar='song_ids', dest='song_ids', nargs='+',
                        help='Download a song list, song_id split by space')
    parser.add_argument('-hot', metavar='artist_id', dest='artist_id',
                        help='Download an artist hot 50 songs by artist_id')
    parser.add_argument('-a', metavar='album_id', dest='album_id',
                        help='Download an album all songs by album_id')
    parser.add_argument('-p', metavar='playlist_id', dest='playlist_id',
                        help='Download a playlist all songs by playlist_id')
    parser.add_argument('-k', metavar='key_word', dest='key_word',
                        help='Download a song by keyword "<songname[\\tsingger]>"')
    parser.add_argument('-kf', metavar='key_word_file', dest='key_word_file',
                        help='Download songs by keyword file "<songname[\\tsingger]>\\n" file encoding UTF-8')
    args = parser.parse_args()
    if args.song_id:
        download_song_by_id(get_parse_id(args.song_id), config.DOWNLOAD_DIR)
    elif args.song_ids:
        for song_id in args.song_ids:
            download_song_by_id(get_parse_id(song_id), config.DOWNLOAD_DIR)
    elif args.artist_id:
        download_hot_songs(get_parse_id(args.artist_id))
    elif args.album_id:
        download_album_songs(get_parse_id(args.album_id))
    elif args.playlist_id:
        download_playlist_songs(get_parse_id(args.playlist_id))
    elif args.key_word:
        download_song_by_key_word(args.key_word, config.DOWNLOAD_DIR)
    elif args.key_word_file:
        file = open(args.key_word_file, mode='r', encoding='UTF-8')
        singger=""
        while 1:
            line = file.readline()
            if not line:
                break
            info = line.split("\t")
            if len(info) > 1:
                singger = info[1]
            download_song_by_key_word(info[0], singger, config.DOWNLOAD_DIR)


"""
use python 3.4.x
"""
if __name__ == '__main__':
    main()
