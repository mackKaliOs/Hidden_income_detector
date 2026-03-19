class TimelineEvent:
    def __init__(self, event_time, description):
        self.event_time = event_time
        self.description = description

class TimelineBuilder:
    def __init__(self):
        self.events = []

    def add_event(self, event_time, description):
        event = TimelineEvent(event_time, description)
        self.events.append(event)

    def get_timeline(self):
        return sorted(self.events, key=lambda event: event.event_time)