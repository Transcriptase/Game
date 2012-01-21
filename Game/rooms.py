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
        #prints description of items and exits
        for i, item in self.items.iteritems():
            if item.type != 'hidden':
                print "There is a %s here." % item.name
        for i, exit in self.exits.iteritems():
            print "There is a %s to the %s." % (exit.name, exit.direction)
        
    def describe_verbose(self):
        #prints the verbose room description
        print self.verbose_description
        self.extra_description()
            
    def describe_terse(self):
        #prints the terse room description
        print self.terse_description
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
    
def create_config_list():
    
    config_list= []
    
    tube_room_config = {
        'label': 'tube_room',
        'verbose_description': """The room is lined with large, glass-fronted tubes like the one
you woke up in. The fluorescent lights flicker on and off, buzzing.
In the center of the room is a metal operating table. A cart of
surgical instruments is overturned nearby.""",
        'terse_description': "You are in an operating room, lined with mysterious person-sized tubes"
        }
    config_list.append(tube_room_config)
    
    central_hallway_west_config = {
        'label': 'central_hallway_west',
        'verbose_description': """The main hallway arcs overhead, and you stand on the western end. The dull thumping of enormous industrial fans
comes from overhead, and their shadows spin crazily on the floor. There's a
wide smear of blood on the grey-green tiles of the floor, starting under one
of the nothern doors and growing gradually thinner as it extends out the main portal
to the east.
""",
        'terse_description': "You are in the western end of the main hallway."
        }
    config_list.append(central_hallway_west_config)
    
    kitchen_config = {
        'label': 'kitchen',
        'verbose_description':"""It seems this was the facility's kitchen. The shelves are lined with empty boxes.""",
        'terse_description': "You are in the kitchen."
        }
    config_list.append(kitchen_config)
    
    central_hallway_east_config = {
        'label': 'central_hallway_east',
        'verbose_description':"""You stand in the eastern half of the central hallway. There's a persistent mechanical hum on the
fringes of your hearing. A thick trail of blood begins under the door to the north and leads out
the main portal, growing thinner as it goes.""",
        'terse_description': "You are in the east half of the main hallway."
        }
    config_list.append(central_hallway_east_config)
    
    return(config_list)
    
def create_room(config):
    new_room = Room()
    new_room.setup(config)
    return(new_room)
    
def populate():
    all_rooms = {}
    config_list = create_config_list()
    for config in config_list:
        new_room = create_room(config)
        all_rooms[new_room.label] = new_room
    return(all_rooms)
            
            
