from functools import wraps
from flask import request

import config

def discord_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Discordbot" not in request.headers.get("User-Agent", "") and not config.DEBUG:
            return "This endpoint is only accessible through Discord", 403
        return func(*args, **kwargs)
    return wrapper
