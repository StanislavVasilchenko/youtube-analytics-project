import json
import os
from googleapiclient.discovery import build
import isodate
import datetime
from src.video import Video, PLVideo


class PlayList(PLVideo):
    api_key = os.getenv("YT_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                          part='snippet, contentDetails',
                                                          maxResults=50,
                                                          ).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        super().__init__(self.video_ids, playlist_id)
        self.title = self.playlist["items"][0]["snippet"]["title"].split(".")[0]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""

        video_response = self.video_response
        all_time = datetime.timedelta()
        for video in video_response['items']:
            print(all_time)
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_time += duration
        return all_time

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        like_video = 0
        best_video = ""
        for v_id in self.video_ids:

            like_count = Video(v_id).likeCount

            if int(like_count) > like_video:
                best_video = f"https://youtu.be/{v_id}"

        return best_video
