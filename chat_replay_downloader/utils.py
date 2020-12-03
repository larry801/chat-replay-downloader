import datetime
import re

def timestamp_to_microseconds(timestamp):
	"""
	Convert RFC3339 timestamp to microseconds.
	This is needed as datetime.datetime.strptime() does not support nanosecond precision.
	"""
	info = list(filter(None, re.split('[\.|Z]{1}', timestamp))) + [0]
	return round((datetime.datetime.strptime('{}Z'.format(info[0]), '%Y-%m-%dT%H:%M:%SZ').timestamp() + float('0.{}'.format(info[1])))*1e6)

def time_to_seconds(time):
	"""Convert timestamp string of the form 'hh:mm:ss' to seconds."""
	return int(sum(abs(int(x)) * 60 ** i for i, x in enumerate(reversed(time.replace(',', '').split(':')))) * (-1 if time[0] == '-' else 1))

def seconds_to_time(seconds):
	"""Convert seconds to timestamp."""
	return re.sub(r'^0:0?', '', str(datetime.timedelta(0, seconds)))

def microseconds_to_timestamp(microseconds, format='%Y-%m-%d %H:%M:%S'):
	"""Convert unix time to human-readable timestamp."""
	return datetime.datetime.fromtimestamp(microseconds//1000000).strftime(format)

def arbg_int_to_rgba(argb_int):
	"""Convert ARGB integer to RGBA array."""
	red = (argb_int >> 16) & 255
	green = (argb_int >> 8) & 255
	blue = argb_int & 255
	alpha = (argb_int >> 24) & 255
	return [red, green, blue, alpha]

def rgba_to_hex(colours):
	"""Convert RGBA array to hex colour."""
	return '#{:02x}{:02x}{:02x}{:02x}'.format(*colours)

def get_colours(argb_int):
	"""Given an ARGB integer, return both RGBA and hex values."""
	rgba_colour = arbg_int_to_rgba(argb_int)
	hex_colour = rgba_to_hex(rgba_colour)
	return {
		'rgba': rgba_colour,
		'hex': hex_colour
	}

# from youtube-dl
def try_get(src, getter, expected_type=None):
    if not isinstance(getter, (list, tuple)):
        getter = [getter]
    for get in getter:
        try:
            v = get(src)
        except (AttributeError, KeyError, TypeError, IndexError):
            pass
        else:
            if expected_type is None or isinstance(v, expected_type):
                return v


def get_title_of_webpage(html):
    match = re.search('<title>(.*?)</title>',html)
    if(match):
        return match.group(1)
    else:
        return None

def int_or_none(v, default=None):
    try:
        return int(v)
    except (ValueError, TypeError):
        return default