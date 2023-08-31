import os
import json
from googleapiclient.discovery import build


class PlayList:
    api_key = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                          part='snippet',
                                                          maxResults=50,
                                                          ).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"].split(".")[0]
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='snippet',
                                                            maxResults=50,
                                                            ).execute()

        print(json.dumps(playlist_videos, indent=2, ensure_ascii=False))
