
# create your own tool through this function

def get_current_datetime():
    import datetime
    now = datetime.datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"