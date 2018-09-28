import json
from pprint import pprint
import sys
import spotipy
import spotipy.util as util

import argparse


class SpotifyConn:
    
    def __init__(self, username):
        self.username = username

        # Init Conn
        self.sp = self.init_conn(self.username)
        self.user_id = self.sp.me()['id']

        self.playlist_name = "Now Playing History"
        self.playlist_tracks = []

    def init_conn(self, username):
        scope = "user-follow-modify"
        token = util.prompt_for_user_token(username,scope,redirect_uri='http://localhost')
        
        if token:
            return spotipy.Spotify(auth=token)
        else: 
            print "Can't get token for ", username
            sys.exit(1)

    def get_playlist_ids(self, exclude_playlist_ids, exclude_playlist_names):
        playlist_ids = []
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] in exclude_playlist_names or playlist['id'] in exclude_playlist_ids:
                continue
            
            playlist_ids.append(playlist['id'])
            
        return playlist_ids
        

    def get_playlist_artists(self, user_id, playlist_id):
        
        tracks = self.sp.user_playlist_tracks(user_id, playlist_id=playlist_id)
        artists = []

        for track in tracks['items']:
            for artist in track['track']['artists']:
                artists.append(artist['id'])

        return artists


    def follow_artists(self, artists):
        self.sp.user_follow_artists(artists)

parser = argparse.ArgumentParser()
parser.add_argument('--user_id')
parser.add_argument('--exclude_playlist_ids')
parser.add_argument('--exclude_playlist_names')
args = parser.parse_args()

if args.exclude_playlist_ids == None:
    args.exclude_playlist_ids = []
else: 
    args.exclude_playlist_ids = args.exclude_playlist_ids.split(',')

if args.exclude_playlist_names == None:
    args.exclude_playlist_names = []
else: 
    args.exclude_playlist_names = args.exclude_playlist_names.split(',')

sp = SpotifyConn(args.user_id)
playlists = sp.get_playlist_ids(args.exclude_playlist_ids, args.exclude_playlist_names)
artists = []
for playlist in playlists:
    artists = artists + sp.get_playlist_artists(args.user_id, playlist)

def unique(list1): 
    unique_list = [] 

    for x in list1: 
        if x not in unique_list: 
            unique_list.append(x) 

    return unique_list

artists = unique(artists)

batches = []
counter = 0
batches.append([])

for index, artist in enumerate(artists):
    if index != 0 and index % 25 == 0:
        counter = counter + 1
        batches.append([])

    batches[counter].append(artist)

for batch in batches:
    if batch:
        sp.follow_artists(batch)

print "Succesfully followed " + len(artists) + " artists!"
