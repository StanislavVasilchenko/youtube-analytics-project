import json
import os
from googleapiclient.discovery import build
import isodate
import datetime


class APIMixin:
    """Класс-миксин для предоставления доступа к API."""

    __API_KEY: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls) -> build:
        """Возвращает объект для работы с API youtube."""
        service = build('youtube', 'v3', developerKey=cls.__API_KEY)
        return service

    def print_info_playlist(self) -> None:
        """Выводит в консоль информацию о плэй-листе."""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        print(json.dumps(playlist_videos, indent=2, ensure_ascii=False))


class PlayList(APIMixin):

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self._init_from_api()

    def _init_from_api(self) -> None:
        """Получаем данные по API и инициализируем ими экземпляр класса."""
        playlist_info = self.get_service().playlists().list(id=self.__playlist_id,
                                                            part='snippet',
                                                            ).execute()
        self.title = playlist_info['items'][0]['snippet']['title'].split(".")[0]
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    def _get_playlist_videos(self) -> dict:
        """Возвращает ответ API на запрос всех видео плей-листа."""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # получит данные по каждому видео
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()
        return video_response

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        print(json.dumps(playlist_videos, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""

        video_response = self._get_playlist_videos()

        duration = datetime.timedelta()
        for video in video_response['items']:
            # Длительности YouTube-видео представлены в ISO 8601 формате
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)

        return duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        video_response = self._get_playlist_videos()

        max_likes = 0
        video_id = ''
        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                video_id = video['id']

        return f'https://youtu.be/{video_id}'
