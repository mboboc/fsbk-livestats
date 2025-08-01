import datetime

def format_duration(td):
    """
    Format a timedelta as M:SS.xxx (e.g., 0:04.554 or 0:04.55 without leading zero in ms)
    """
    if td is None:
        return None
    total_seconds = int(td.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    milliseconds = int(round(td.microseconds / 1000.0))

    # Handle rounding overflow
    if milliseconds == 1000:
        seconds += 1
        milliseconds = 0
    if seconds == 60:
        minutes += 1
        seconds = 0

    # Drop leading zeros from milliseconds (strip left zeroes)
    ms_str = str(milliseconds).lstrip('0')
    return f"{minutes}:{seconds:02d}.{ms_str}"