from django.core.cache import cache
from config.settings import USE_CACHE


def check_cache(key):
    def func_check_cache(func):
        def checking(self):
            if not USE_CACHE:
                data = func(self)
                return data
            else:
                cache_data = cache.get(str(self.id) + key)
                if cache_data is None:
                    data = func(self)
                    cache.set(str(self.id) + key, data, timeout=1)
                    return data
                else:
                    return cache_data
        return checking
    return func_check_cache