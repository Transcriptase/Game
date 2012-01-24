import items
import csv

class Exit(items.Item):
    def exit_setup(self, config):
        self.config = config
        self.abbreviations = {
            'north': 'n',
            'south': 's',
            'east': 'e',
            'west': 'w'
            }
        
        self.setup(self.config)
        #sets up the properties that Exits share with Items
        if config['is_open'] == 'yes':
            self.is_open = True
        else:
            self.is_open = False
        #necessary because the CSV import is a string, not a boolean
            
        self.direction = config['direction']
        self.destination = config['destination']
        
        self.keywords.append(self.direction)
        self.keywords.append(self.abbreviations[self.direction])
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
        self.player = player
        if self.player.inventory.has('keycard') and self.player.inventory.has('parka'):
            self.is_open = True
            return(True)
        elif self.player.inventory.has('keycard'):
            print """
    The reader beeps as the light turns green, and the door swings open. Outside, a howling wind whips
    across waist-deep drifts of snow. It's hard to see anything through the blizzard. You don't think
    you'd survive long out there without some protection from the cold.
            """
            return(False)
        else:
            print "You think you'll need a keycard to open that door."
            return(False)
            
    def reactor_special(self, player):
        self.player = player
        if self.player.injected == False:
            print "You really don't think it's a good idea to go in there unprotected."
            return False
        else:
            print "You step through the door. You're pretty sure that you wouldn't experience radiation exposure as a slight subdermal tingle, so that's probably your imagination."
            return True
            
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
    all_exits['main_portal_rev'].shall_pass = all_exits['main_portal'].main_portal_special
    all_exits['reactor_door'].shall_pass = all_exits['reactor_door'].reactor_special
    all_exits['reactor_door_rev'].shall_pass = all_exits['reactor_door'].reactor_special
    return(all_exits)
    
    
def populate():
    all_exits = {}
    f = open('data/exits.csv', 'rb')
    reader = csv.DictReader(f)
    
    for config in reader:
        config['keywords'] = config['keywords'].split()
        config['use_words'] = config['use_words'].split()
        #make entries into lists before passing to creation function
        
        new_exit = create_exit(config)
        all_exits[new_exit.label] = new_exit
        reverse_exit = create_exit(create_config_reverse(config))
        all_exits[reverse_exit.label] = reverse_exit
    all_exits = special_setup(all_exits)
    return(all_exits)