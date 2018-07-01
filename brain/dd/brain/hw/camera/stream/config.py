from attr import attrib, attrs


@attrs
class VideoStreamConfig:
    type = attrib()

    width = attrib()
    height = attrib()
    framerate = attrib(default=None)

    name = attrib(default='video_stream')

    flip_horizontal = attrib(default=False)
    flip_vertical = attrib(default=False)
    rotate_cw_muliplier = attrib(default=0)

    source_number = attrib(default=0)

    @property
    def resolution(self):
        return self.width, self.height


default_config = VideoStreamConfig(
    type='pi',
    width=320,
    height=240,
)
