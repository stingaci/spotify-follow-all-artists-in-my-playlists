# spotify-follow-all-artists-in-my-playlists

This is a simple script that will go through your playlists and follows all the artists within them (in case you either forgot to, or used a playlist sync tool when you first started using Spotify). 

Usage: 

`python syncer.py --user_id USER_ID --exclude_playlist_names 'COMMA_SEPARATED_PLAYLIST_NAMES' --exclude_playlist_ids 'COMMA_SEPARATED_PLAYLIST_IDS'`

`exclude_playlist_names` and `exclude_playlist_ids` are optional. **If your playlist name has a comma in it, the exclusion rules will fail!!!** One day, I'll clean this up

Other notes: 

* You will need a Client ID and Client Secret from Spotify. Use Env vars to supply them

