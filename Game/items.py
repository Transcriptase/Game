class Item(object):
    #properties of all items

    def setup(self, config):
        # Takes in a dictionary and assigns item properties according to labels
        self.config = config
        
        self.label = config['label']
        #one word, serves as key in dictionary and shortest name
        
        self.name = config['name']
        #short descriptive phrase
        
        self.description = config['description']
        #full detailed descriptive text
        
        self.location = config['location']
        #string matching label of starting room
        
        self.keywords = config['keywords']
        #a list of synonyms and other words that would help identify it
        
        self.type = config['type']
        # possible values: "carryable", "exit", "scenery", "hidden"
        
        self.look_special = config['look_special']
        #change this flag to true to trigger special room-specific events when the item
        #is examined

# Sets up item objects by creating a config dictionary for each one
# 
# Sample config dictionary (can be copied for each new item):
#config = {
#   'label':'LABEL',
#   'name':'NAME',
#   'description':'DESCRIPTION',
#   'location':'LOCATION',
#   'keywords':['KEYWORD1'],
#   'type':'TYPE'
#   'look_special': False
#}

#'label' : a single word string used as an internal id
#'name': the user-facing name of the item
#'decription': the full verbose description
#'location': the label of the starting room
#'keywords': a list of keywords that the player might refer to the item as
#'type': a flag that determines properties. Possible values: "carryable", "scenery", "exit", "hidden"
#'look_special": set to True to trigger room-specific events when the item is examined

def create_config_list():
    #create a list of config vectors for each item
    #to create a new item, make a config vector and add it to the list
    config_list = []
    scalpel_config = {
        'label':'scalpel',
        'name':'sharp scalpel',
        'description':"""The scalpel is sharp, but flecks of rust-colored blood hint that it's been used.""",
        'location':'tube_room',
        'keywords':['scalpel'],
        'type':'carryable',
        'look_special':False
    }
    config_list.append(scalpel_config)
    
    corpse_config = {
        'label':'corpse',
        'name':'twisted corpse',
        'description':"""
The body is twisted unaturally, but there's no blood, except on his hands.
He is wearing a lab coat.
His pockets are stuffed with energy bars and dried food.
His keycard hangs from a lanyard around his neck.
        """,
        'location':'kitchen',
        'keywords':['corpse', 'body'],
        'type':'scenery',
        'look_special': True
    }
    config_list.append(corpse_config)
    
    keycard_config = {
        'label':'keycard',
        'name':'keycard',
        'description':"""
The dead scientist's keycard.
        """,
        'location':'kitchen',
        'keywords':['keycard', 'key', 'card'],
        'type':'hidden',
        'look_special': False
    }
    config_list.append(keycard_config)
    
    
    return(config_list)
 
    
    
def create_item(config):
    new_item = Item()
    new_item.setup(config)
    return(new_item)

def populate():
    #runs each of the item creation functions
    #and returns a dictionary of all the items
    all_items = {}
    config_list = create_config_list()
    for config in config_list:
        new_item = (create_item(config))
        all_items[new_item.label] = new_item
    return(all_items)
    