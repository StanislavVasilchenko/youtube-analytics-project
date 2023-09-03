import json
import os

from googleapiclient.discovery import build

from src.video import PLVideo
import isodate
import datetime


class PlayList(PLVideo):
    api_key = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                          part='snippet, contentDetails',
                                                          maxResults=50,
                                                          ).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"].split(".")[0]
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='snippet, contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        print(json.dumps(playlist_videos, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        all_time = datetime.timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_time += duration
        return all_time

# pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
# # # pl.print_info()
# pl.total_duration()
