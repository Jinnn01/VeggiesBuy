
class Reciept:
    def __init__(self, store = None, location = None, timestamp = None, items = []):
        self.store = store
        self.location = location
        self.timestamp = timestamp
        self.items = items

    def __json__(self):
        return{
            "store_name": self.store,
            "location": self.location,
            "timestamp": self.timestamp,
            "items": self.items
        }

    def __repr__(self):
        return f'{self.store}, {self.location}, {self.timestamp}, {self.items}'

    def __str__(self):
        return f'Store: {self.store} \nLocation: {self.location} \ntimestamp: {self.timestamp} \nItems: {self.items}' 

    def clear(self):
        self.store = None
        self.location = None
        self.timestamp = None
        self.items = []
        return
