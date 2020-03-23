from typing import Optional

from django.utils import timezone

from request_logging.base import append_to_list, retrieve
from request_logging.models import RequestLog
import logging

logger = logging.getLogger("ablator.functionality")
LOK_KEY = "list-of-timestamp-keys"


def save_new_timestamp_key(new_key):
    append_to_list(LOK_KEY, new_key)


def list_timestamp_keys():
    return retrieve(LOK_KEY)


def generate_key_for_id_hourly(func_id: str, timestamp=None):
    """
    Generate a string to be used as key for grouping request logs. The string is returned, and it
    is stored in the list of existing valid keys.

    :param func_id: A functionality id
    :param timestamp: a DateTime object for the requested timestamp
    :return: A string to be used as key. Contains the year, month, day, and hour of the timestamp
    """
    time_stamp_for_key = timestamp if timestamp else timezone.now()
    current_key = "{}-{}".format(func_id, time_stamp_for_key.strftime("%Y-%m-%d-%H"))
    save_new_timestamp_key(current_key)
    return current_key


def save_request_log_entry(
    functionality_id: str, flavor_id: Optional[str], action: str, client_user_id: str = None, elapsed_time: float = None
):
    current_key = generate_key_for_id_hourly(functionality_id)
    timestamp = timezone.now()
    f_action = {
        "functionality_id": functionality_id,
        "flavor_id": flavor_id,
        "timestamp": timestamp,
        "action": action,
        "client_user_id": client_user_id,
        "elapsed_time": elapsed_time,
    }
    append_to_list(current_key, f_action)
    logger.info(action, extra=f_action)


def get_request_logs(timestamp_key):
    request_log_dicts = retrieve(timestamp_key)
    request_logs = [
        RequestLog(d["functionality_id"], d["flavor_id"], d["timestamp"], d["action"], d["client_user_id"], d["elapsed_time"])
        for d in request_log_dicts
    ]
    return request_logs


def get_request_logs_for_functionality_id(functionality_id):
    timestamp_keys = list_timestamp_keys()
    logs = {}
    for timestamp_key in timestamp_keys:
        if functionality_id in timestamp_key:
            logs[timestamp_key] = get_request_logs(timestamp_key)
