import items

class Exit(items.Item):
    def exit_setup(self, config):
        self.config = config
        
        self.setup(self.config)
        #sets up the properties that Exits share with Items
        
        self.is_open = config['is_open']
        self.direction = config['direction']
        self.destination = config['destination']
        #sets up the exit-specific properties
        
# Sets up exit objects by creating a config dictionary for each one
# 
# Sample config dictionary (can be copied for each new item):
#config = {
#   'label':'LABEL',
#   'name':'NAME',
#   'description':'DESCRIPTION',
#   'location':'LOCATION',
#   'keywords':['KEYWORD1'],
#   'type':'exit',
#   'look_special': False,
#   'is_open':True,
#   'direction':'DIRECTION',
#   'destination':'destination'
#}

#'label' : a single word string used as an internal id
#'name': the user-facing name of the item
#'decription': the full verbose description
#'location': the label of the starting room
#'keywords': a list of keywords that the player might refer to the item as
#'type': a flag that determines properties. All exits are type 'exit'.
#'look_special": set to True to trigger room-specific events when the item is examined
#'is_open': True allows free passage, False is closed
#'direction': The direction of the exit (cardinals or up/down)
#'destination': a string matching the label of the room the exit leads to
    
    def shall_pass(self, player):
        #by default, checks the "is_open" flag and acts accordingly
        #to make more complex behavior, this method can be swapped out during setup
        #add the method to the SpecialFunctionDonor class, then overwrite the default
        #function with the function from the donor in special_setup
        self.player = player
        
        if self.is_open == True:
            return(True)
        else:
            print "The %s is closed." #shouldn't happen
            return(False)
            
#to create custom "shall pass" behavior, make a substitute method below
#then alter the special_setup function to swap the new method for that particular
#Exit object's "shall_pass" attribute.

    def main_portal_special(self, player):
        if player.inventory.has('keycard') and player.inventory.has('parka'):
            self.is_open = True
            return(True)
        elif player.inventory.has('keycard'):
            print """
The reader beeps as the light turns green, and the door swings open. Outside, a howling wind whips
across waist-deep drifts of snow. It's hard to see anything through the blizzard. You don't think
you'd survive long out there without some protection from the cold.
            """
            return(False)
        else:
            print "You think you'll need a keycard to open that door."
            return(False)
            
        

def create_config_list():
    #To create an exit, make a config vector and add it to the config list
    
    config_list = []
    
    tube_to_hall_config = {
        'label':'tube_to_hall',
        'name':'pair of double doors',
        'description':"""
The double doors are heavy, with high circular windows lined with chicken wire.""",
        'location':'tube_room',
        'keywords':["door", "doors", "north", "n"],
        'type':'exit',
        'look_special': False,
        'is_open':True,
        'direction':'north',
        'destination':'central_hallway_west'
    }
    config_list.append(tube_to_hall_config)
    
    hall_to_kitchen_config = {
        'label':'hall_to_kitchen',
        'name':'broken door hanging from its hinges',
        'description':"""
The door seems to have been locked, but then broken open from the outside. The metal is dented.""",
        'location':'central_hallway_west',
        'keywords':["broken", "north", "n"],
        'type':'exit',
        'look_special': False,
        'is_open':True,
        'direction':'north',
        'destination':'kitchen'
    }
    config_list.append(hall_to_kitchen_config)
    
    hall_link_config = {
        'label':'hall_link',
        'name':'hallway stretching off',
        'description':"""
The hallway stretches out to the east. It's dim, but you can see more doors and a looming main portal in the distance.""",
        'location':'central_hallway_west',
        'keywords':["hall", "east", "e"],
        'type':'exit',
        'look_special': False,
        'is_open':True,
        'direction':'east',
        'destination':'central_hallway_east'
    }
    config_list.append(hall_link_config)
    
    main_portal_config = {
        'label':'main_portal',
        'name':'huge set of sliding steel doors, with a card reader nearby',
        'description':"""
This looks like the main entrance to the facility. Two enormous slabs of metal, with
black rubber covering every possible seam. A card reader blinks red beside it.
        """,
        'location':'central_hallway_east',
        'keywords':["main", "sliding", "e"],
        'type':'exit',
        'look_special': False,
        'is_open':False,
        'direction':'east',
        'destination':'outside'
    }
    config_list.append(main_portal_config)
    
    failure_config = {
        'label' : 'not_found',
        'name':'not found',
        'description':"A dummy item to be passed when search fails",
        'location':'',
        'keywords':[],
        'type':'hidden',
        'look_special': False,
        'is_open':False,
        'direction':'east',
        'destination':''
    }
    config_list.append(failure_config)
        
    
    return(config_list)
    
    
    
def create_exit(config):
    new_exit = Exit()
    new_exit.exit_setup(config)
    return(new_exit)
    
def reverse_direction(word):
    #if the string is a direction, returns its opposite
    #otherwise, returns the string
    reversal_guide = dict({
        "north":"south", 
        "south":"north",
        "east":"west",
        "west":"east", 
        "up":"down",
        "down":"up",
        "n":"s",
        "s":"n",
        "e":"w",
        "w":"e"
    })
    
    if word in reversal_guide:
        word = reversal_guide[word]
    return(word)
    
def create_config_reverse(config):
    #allows quick set-up of both sides of an exit
    #swaps location and destination and reverses direction
    
    
    config['label'] = config['label']+"_rev"
    
    old_destination = config['destination']
    old_location = config['location']
    old_keywords = config['keywords']
    config['direction'] = reverse_direction(config['direction'])
    config['location'] = old_destination
    config['destination'] = old_location
    
    new_keywords = []
    for keyword in old_keywords:
        new_keywords.append(reverse_direction(keyword))
    config['keywords'] = new_keywords
        
    return(config)
    
def special_setup(all_exits):
    all_exits['main_portal'].shall_pass = all_exits['main_portal'].main_portal_special
    return(all_exits)
    
    
def populate():
    all_exits = {}
    config_list = create_config_list()
    for config in config_list:
        new_exit = create_exit(config)
        all_exits[new_exit.label] = new_exit
        reverse_exit = create_exit(create_config_reverse(config))
        all_exits[reverse_exit.label] = reverse_exit
    all_exits = special_setup(all_exits)
    return(all_exits)