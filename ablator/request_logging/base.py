from django.core.cache import cache
from django.conf import settings
from django.utils import timezone


# Private Methods
def _save(k, v):
    cache.set(k, v, settings.ACTIVATION_LOGGING_CACHE_TIMEOUT)


def _retrieve(k):
    return cache.get(k)


def _retrieve_or_save(k, default_v):
    return cache.get_or_set(k, default_v, timeout=settings.ACTIVATION_LOGGING_CACHE_TIMEOUT)


def _increase(k):
    cache.incr(k)


def _append(list_key, v):
    the_list = cache.get_or_set(list_key, [], timeout=settings.ACTIVATION_LOGGING_CACHE_TIMEOUT)
    the_list.append(v)
    _save(list_key, the_list)


def _update_timestamp(k):
    cache.get_or_set(k, timezone.now, timeout=settings.ACTIVATION_LOGGING_CACHE_TIMEOUT)


# Public Methods
def update_dict(dict_key, k, v):
    the_dict = _retrieve_or_save(dict_key, {})
    the_dict[k] = v
    _save(dict_key, the_dict)


def append_to_list(list_key, v):
    current_list = _retrieve_or_save(list_key, [])
    if v not in current_list:
        _append(list_key, v)


def retrieve(k):
    return _retrieve(k)
