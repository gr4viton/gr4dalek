from threading import Thread


class VideoStreamBase:

    def __init__(self, config):
        self.config = config
        self.running = False

        self._pre_config(config)
        self._base_start_stream()
        self._post_config(config)

    def _pre_config(self, config):
        """Configure camera before stream start."""
        pass

    def _base_start_stream(self):
        """Start camera stream after its _pre_config."""
        self._start_stream()
        self.running = True

    @property
    def stopped(self):
        return not self.running

    @property
    def name(self):
        name = self.config.name
        if not name:
            name = self.title
        return name

    def _post_config(self, config):
        """Configure camera after stream start."""
        pass

    def start(self):
        """Start the thread to read frames from the video stream."""
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()

    def update(self):
        """Function to run in separate thread which updates the self.fram with actual camera capture."""
        self._update()
