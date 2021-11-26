import time
from datetime import datetime


class SpiderCount:

    def __init__(
            self,
            name: str,
            time_start: datetime,
            time_end: datetime,
            success: int = 0,
            failure: int = 0
    ):
        self._name = name
        self._time_start = time_start.strftime('%Y-%m-%d %H:%M:%S')
        self._time_end = time_end.strftime('%Y-%m-%d %H:%M:%S')
        self._success = success
        self._failure = failure

    def __repr__(self):
        return f"【name: {self._name}, time_start: {self._time_start}, time_end: {self._time_end}, " \
               f"success: {self._success}, failure: {self._failure}】"

    def do_dump(self):
        elements = [one for one in dir(self) if not (one.startswith('__') or one.startswith('_') or one.startswith('do_'))]
        data = {}
        for name in elements:
            data[name] = getattr(self, name, None)
        data['_id'] = str(int(time.time() * 1000))
        return data

    @property
    def name(self):
        return self._name

    @property
    def time_start(self):
        return self._time_start

    @property
    def time_end(self):
        return self._time_end

    @property
    def success(self):
        return self._success

    @property
    def failure(self):
        return self._failure
