class SimpleDataCache:
    def __init__(self, debug=False):
        self.data_dict = {}
        self.debug = debug

    def getOrLoad(self, key, func, *args):
        result = self.get(key)
        if result is None:
            return self.load(key, func(*args))
        else:
            return result

    def load(self, key, obj):
        self._debug('cache load')
        self.data_dict[key] = obj
        return obj

    def get(self, key):
        if key in self.data_dict:
            self._debug('cache hit')
            return self.data_dict[key]
        else:
            self._debug('cache miss')
            return None

    def clear(self):
        self.data_dict.clear()

    def _debug(self, msg):
        if self.debug is True:
            print(msg)
