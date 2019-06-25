"""Helper for working with lukas."""
import urllib.error
import urllib.request
from ilswbot.config import config


def get_lukas_status():
    """Poll the ilsw api for lukas's sleep status."""
    try:
        status = urllib.request.urlopen(config['settings']['api_url']).read()
        return True, status.decode('utf-8')
    except (urllib.error.HTTPError, urllib.error.URLError):
        return False, 'Jo. Die Api ist im Sack.'


def status_changed(status):
    """Check if the sleeping status of lukas changed."""
    # Determine status by response.
    # If an invalid response is returned we instantly return False
    if status.lower() == 'ja':
        status = True
    elif status.lower() == 'nein':
        status = False
    else:
        return False

    global sleeping
    if sleeping is None:
        sleeping = status
        return False

    if sleeping == status:
        return False
    else:
        sleeping = status
        return True
