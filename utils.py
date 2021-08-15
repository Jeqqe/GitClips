"""
@File: utils.py
@Description: helpful methods
"""

from datetime import datetime

# Logger
def log(msg):

    now = datetime.now()
    formatted_time = now.strftime('%m/%d/%Y, %H:%M:%S')
    print(f'[{formatted_time}] GitClips > {msg}')