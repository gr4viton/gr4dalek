from .pi import VideoStreamPi
from .cv import VideoStreamCV
from .config import default_config


class VideoStreamSelector:

    def __init__(self):
        raise NotImplementedError('use from_config method to initialize.')

    @staticmethod
    def from_config(video_config=default_config):
        if video_config.type == 'pi':
            Stream = VideoStreamPi
        elif video_config.type == 'cv':
            Stream = VideoStreamCV

        return Stream(video_config)
