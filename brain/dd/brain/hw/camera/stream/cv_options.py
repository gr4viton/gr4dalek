import cv2
from enum import Enum


class OpenCVEnum(Enum):
    pass


class VideoCaptureProperty(Enum):

    def __init__(self):
        prefix = 'CAP_PROP'
        arg_map = {
            arg: getattr(cv2, arg) for arg in dir(cv2)
            if arg.startswith(prefix)
        }

        enum_map = {
            value: arg[len(prefix):].lower() for arg, value in arg_map.items
        }

        for value in sorted(list(enum_map.keys())):
            enum_name = enum_map[value]
            setattr(self, enum_name, value)

        super(VideoCaptureProperty, self).__init__()
