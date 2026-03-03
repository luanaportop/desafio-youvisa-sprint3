subscribers = {}

def subscribe(event_type, handler):

    if event_type not in subscribers:
        subscribers[event_type] = []

    subscribers[event_type].append(handler)

def publish(event_type, data):

    if event_type in subscribers:
        for handler in subscribers[event_type]:
            handler(data)