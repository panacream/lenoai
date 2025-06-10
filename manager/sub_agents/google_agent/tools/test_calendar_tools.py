import json
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from calendar_tools import list_upcoming_events

def test_list_upcoming_events():
    events = list_upcoming_events()
    print(json.dumps(events, indent=2))

if __name__ == "__main__":
    test_list_upcoming_events()
