class EventBus(object):

    def __init__(self):
        super(EventBus, self).__init__()
        self.events = {}

    def filter_events(self, event):
        if event.key not in self.events:
            return
        if type(self.events[event.key]) == list:
            for x in self.events[event.key]:
                print type(x)
                return x(event)
        else:
            print type(self.events[event.key](event))
            return self.events[event.key](event)

    def subscribe(self, key, view_response):
        if key not in self.events.keys():
            self.events.update({str(key): view_response})
        else:
            if type(self.events[key]) == list:
                self.events[key].append(view_response)
            else:
                self.events[key] = [self.events[key], view_response]


class StandardFrbLink(EventBus):

    def __init__(self, frb_view_list):
        super(StandardFrbLink, self).__init__()
        for y in frb_view_list:
            self.subscribe('i', y.zoom_in)
            self.subscribe('o', y.zoom_out)
            self.subscribe('h', y.pan_left)
            self.subscribe('j', y.pan_down)
            self.subscribe('k', y.pan_up)
            self.subscribe('l', y.pan_right)

        for frb_view in frb_view_list:
            frb_view.fig.canvas.mpl_connect('key_press_event',
                                            self.filter_events)
