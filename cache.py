import time
import redis

class SimpleCache:
    def __init__(self, debug=False):
        self._data_dict = {}
        self._debug = debug

    def getOrLoad(self, key, func, *args):
        result = self.get(key)
        if result is None:
            return self.load(key, func(*args))
        else:
            return result

    def load(self, key, obj):
        self._debugLog('cache load')
        self._data_dict[key] = obj
        return obj

    def get(self, key):
        if key in self._data_dict:
            self._debugLog('cache hit')
            return self._data_dict[key]
        else:
            self._debugLog('cache miss')
            return None

    def clear(self):
        self._data_dict.clear()

    def _debugLog(self, msg):
        if self._debug is True:
            print(msg)


class TTLCache(SimpleCache):
    def __init__(self, evictAfterMinutes, debug=False):
        super().__init__(debug)
        self._evict_after_minutes = evictAfterMinutes

    def load(self, key, obj):
        return super().load(key, CachedData(data=obj, cachedAt=time.time())).get_data()

    def get(self, key):
        cached_data_obj = super().get(key)
        if cached_data_obj is not None:
            current_time = time.time()
            data_time = cached_data_obj.get_time()
            diff_in_seconds = current_time-data_time
            diff_in_minutes = divmod(diff_in_seconds, 60)[0]
            if diff_in_minutes >= self._evict_after_minutes:
                self._debugLog("evict")
                del self._data_dict[key]
                return None
            return cached_data_obj.get_data()
        else:
            return None


class CachedData:
    def __init__(self, data, cachedAt):
        self._data = data
        self._time = cachedAt

    def get_data(self):
        return self._data

    def get_time(self):
        return self._time  
