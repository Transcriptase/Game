import csv

class Room(object):
    #organizes and manipulates rooms
    
    def __init__(self):
        self.visits = 0
        
    def setup(self, config):
        self.config = config
        
        self.label = config['label']
        self.verbose_description = config['verbose_description']
        self.terse_description = config['terse_description']
        
        
    def extra_description(self):
        print '\n'
        #prints description of items and exits
        for i, item in self.items.iteritems():
            if item.type != 'hidden':
                print "There is a %s here." % item.name
        for i, exit in self.exits.iteritems():
            print "There is a %s to the %s." % (exit.name, exit.direction)
        
    def describe_verbose(self):
        #prints the verbose room description
        print "\n%s" % self.verbose_description
        self.extra_description()
            
    def describe_terse(self):
        #prints the terse room description
        print "\n%s" % self.terse_description
        self.extra_description()
        
    def describe(self):
        #the main description printing function:
        #checks to see if the player has been here before
        #prints the verbose description on the first visits
        #and the terse description on all others. Always prints
        #descriptions of items and exits.
        if self.visits == 0:
            self.describe_verbose()
            self.visits += 1
        else:
            self.describe_terse()
            
    def add_items(self, item_list):
    #iterates through the item dictionary and makes a new dictionary
    #of items whose location matches the room
        self.item_list = item_list
        self.items = {}
        for key, item in self.item_list.iteritems():
            if item.location == self.label:
                self.items[item.label] = item
                
    def add_exits(self, exit_list):
        self.exit_list = exit_list
        self.exits = {}
        for key, exit in self.exit_list.iteritems():
            if exit.location == self.label:
                self.exits[exit.label] = exit
    
    
def create_room(config):
    new_room = Room()
    new_room.setup(config)
    return(new_room)
    
def populate():
    all_rooms = {}
    f = open("data/rooms.csv", "rb")
    reader = csv.DictReader(f)
    
    for config in reader:
        new_room = create_room(config)
        all_rooms[new_room.label] = new_room
    return(all_rooms)