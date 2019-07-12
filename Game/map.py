from . import items
from . import exits
from . import rooms

class Map(object): 
    def setup(self):
        self.all_items = items.populate()
        self.all_exits = exits.populate()
        self.all_rooms = rooms.populate()
        
        for label, room in self.all_rooms.items():
            room.add_items(self.all_items)
            room.add_exits(self.all_exits)