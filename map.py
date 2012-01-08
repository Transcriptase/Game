class Item(object):
    #properties of all items
    def __init__(
        self,
        label,
        name,
        description,
        location,
        keywords,
        type,
        look_special = False
        ):
        self.label = label
        #one word, serves as key in dictionary and shortest name
        self.name = name
        #short descriptive phrase
        self.description = description
        #full detailed descriptive text
        self.location = location
        #string matching label of starting room
        self.keywords = keywords
        #a list of synonyms and other words that would help identify it
        self.type = type
        # possible values: "carryable", "exit", "scenery", "hidden"
        self.look_special = look_special
        #change this flag to true to trigger special room-specific events when the item
        #is examined
        
class Exit(Item):
    # I realized exits were very similar to items and could be created and placed similarly
    def __init__(
        self,
        label,
        name,
        description,
        location,
        keywords,
        is_open,
        direction,
        destination
        ):
        #gotta import the item attributes initially
        if hasattr(Item, '__init__'):
            Item.__init__(
                self,
                label,
                name,
                description,
                location,
                keywords,
                type = "exit",
                look_special = False
                )
                    
        #these are different from items
        self.is_open = is_open
        self.direction = direction
        self.destination = destination 
        #this needs to be a string that matches the label of the room it leads to
        
class MainPortal(Exit):
    #seems like the best way to implement complicated exit behavior is by tacking on
    #a function as part of a subclass. then i can check for the exitence of the
    #move_special attribute, then run it.
    def move_special(self, inventory):
        self.inventory = inventory
        if ("keycard" in self.inventory.inventory.keys()) and ("parka" in self.inventory.inventory.keys()):
            self.is_open = True
            return("outside")
        if ("keycard" in self.inventory.inventory.keys()):
            print """
  The reader beeps as the light turns green, and the door swings open. Outside, a howling wind whips
  across waist-deep drifts of snow. It's hard to see anything through the blizzard. You don't think
  you'd survive long out there without some protection from the cold.
            """
            return("central_hallway_east")
        else:
            print "You think you'll need a keycard to open that door."
            return("central_hallway_east")
    
        
        
        
        
class Inventory(object):
    #manages the player's inventory
    #creates a dictionary using an item's label as the key
    #linked to the Item-class object
    
    def __init__(self):
        self.inventory = {}
        #this is the inventory dictionary
        
    def pick_up(self, item, room_items):
        # adds an item to the inventory dictionary
        # and removes it from the room's item list dictionary
        self.item = item
        self.room_items = room_items
        
        print "You pick up the %s." % self.item.name
        self.inventory[self.item.label]= self.item
        del self.room_items[self.item.label]
        
    def drop(self, item, room_items):
        # removes an item from the inventory dictionary
        # and adds it to the room's item list dicitonary
        self.item = item
        self.room_items = room_items
        
        print "You drop the %s." % self.item.name
        
        self.room_items[self.item.label]=self.item
        del self.inventory[self.item.label]
        
    def look(self, command):
        #allows use of the look command on carried items
        self.command = command
        self.item_to_describe = mentioned_in(self.command, self.inventory)
        if self.item_to_describe == "not_found":
            return False
        elif self.item_to_describe.look_special == True:
            print self.item_to_describe.description
            return True
            self.look_special(self.item_to_describe.label)
            #not necessary to pass the item label currently b/c there's only
            #one special event per room, but that could change.
        else:
            print self.item_to_describe.description
            return True
            
    def list(self):
    #lists the contents of the inventory, responds appropriately if inventory is empty
        if self.inventory == {}:
            print "You are not carrying anything."
        else:
            print "You are carrying:"
        for i, item in self.inventory.iteritems():
            print item.name
            
class Mobile(object):
    #a class for things that move around. Right now that's just the player.
    #tracks inventory and location
    
    def __init__(self, inventory):
        self.inventory = inventory
        self.location = "tube_room"
        #a placeholder that's replaced by a room object as soon as it's called
        self.new_location = "tube_room"
        #NOT A ROOM OBJECT, just a string matching the label of a room object
        #the engine's move_into function makes the new player.location
        #be the room that matches the label
        
        
    def movement(self, action):
        #called if the command starts with a movement keyword
        #compares the content of the command to the keywords for
        #each exit in the room
        self.command = action
        self.exit_to_try = mentioned_in(self.command, self.location.exits)
        if self.exit_to_try == "not_found":
            print "You can't go there."
        # check to see if the exit is valid/open
        elif self.exit_to_try.is_open == False:
            if hasattr(self.exit_to_try, 'move_special'):
                self.new_location = self.exit_to_try.move_special(self.inventory)
            else:
                print "The %s is closed for now." % self.exit_to_try.name
        else:
            print "You go through the %s to the %s." % (self.exit_to_try.name, self.exit_to_try.direction)
            self.new_location = self.exit_to_try.destination
    
    def inventory_take(self, action):
        #called if the player is trying to pick something in the room up
        #checks to see if the item (last word of the command) is there,
        #then calls the pick up function if it finds it. If not, engages the failure function
        #current failure function is boring.
        self.command = action
        self.success = False
        
        self.item_to_try = mentioned_in(self.command, self.location.items)
        if self.item_to_try == "not_found":
            print "I don't see one of those to pick up."
        elif self.item_to_try.type != "carryable":
            print "You can't pick that up."
        else:   
            self.inventory.pick_up(self.item_to_try, self.location.items)
            
    def inventory_drop(self, action):
        #called if the player is trying to drop something
        #reverse of  inventory_take.
        
        self.command = action
        
        self.item_to_try = self.mentioned_in(self.command, self.inventory.inventory)
            #have to call the inventory dictionary from 
            #inside the inventory class. confusing names
        self.inventory.drop(self.item_to_try, self.location.items)
                    
            
    def look(self, command):
        #similar to the movement and inventory functions
        #but called when a look keyword is entered and
        #prints the full description of any recognized item
        
        self.command = command
        
        #exits are items and have descriptions, so best would be to
        #combine the two dictionaries before passing
        
        self.things_to_look_at = dict(self.location.items.items())
        self.things_to_look_at.update(self.location.exits)
        #and here naming the dict of items "items" gets awkward
        #first line calls the items() property of the dictionary named "items"
        #second line mixes in the exits dictionary
        #this seems awkward but was the best way i could come up with to
        #add two dicts while leaving the originals intact
        
        self.item_to_describe = mentioned_in(self.command, self.things_to_look_at)
        if self.item_to_describe == "not_found":
            return False
        elif self.item_to_describe.look_special == True:
            print self.item_to_describe.description
            self.location.look_special(self.item_to_describe.label)
            return True
            #not necessary to pass the item label currently b/c there's only
            #one special event per room, but that could change.
        else:
            print self.item_to_describe.description
            return True
        

class ItemsInitializer(object):
    #creates each item and puts it in a dictionary to pass to the map class
    #modular design: each item has a function that defines its variables
    #and creats an Item-class object with those variables, and adds it to a main dictionary
    #Then the populator runs each item creation function and returns the dictionary
    def __init__(self):
        self.all_items = {}
        #the dictionary containing all the items
        

        
    def create_exit_reverse(self, label, exit):
        #allows quick set-up of both sides of an exit
        #swaps location and destination and reverses direction
        self.label = label
        self.exit = exit
        self.reversal_guide = dict({"north":"south", 
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
        self.reversed_location = self.exit.destination
        self.reversed_destination = self.exit.location
        self.reversed_direction = self.reversal_guide[self.direction]
        self.reversed_keywords = []
        for keyword in self.exit.keywords:
            if keyword in self.reversal_guide:
                self.reversed_keywords.append(self.reversal_guide[keyword])
            else:
                self.reversed_keywords.append(keyword)
        self.reversed_exit = Exit(
            self.exit.label,
            self.exit.name,
            self.exit.description,
            self.reversed_location,
            self.reversed_keywords,
            self.exit.is_open,
            self.reversed_direction,
            self.reversed_destination
            )
        self.all_items[self.label] = self.reversed_exit
            
    def create_tube_to_hall_doors(self):
        #create the exit leading from tube room to central hallway
        #all exit creation functions also create the reverse exit
        self.label = "tube_to_hall_doors"
        self.name = "a pair of double doors"
        self.description = "The double doors are heavy, with high circular windows lined with chicken wire."
        self.keywords = ["door", "doors", "north", "n"]
        self.direction = "north"
        self.location = "tube_room"
        self.destination = "central_hallway_west"
        self.is_open = True
        self.tube_to_hall_doors = Exit(
            self.label,
            self.name,
            self.description,
            self.location,
            self.keywords,
            self.is_open,
            self.direction,
            self.destination
            )
        self.all_items[self.label] = self.tube_to_hall_doors
        self.create_exit_reverse("hall_to_tube_doors", self.tube_to_hall_doors)
        
    def create_hall_to_kitchen_door(self):
        self.label = "hall_to_kitchen_door"
        self.name = "a broken door hanging from its hinges"
        self.description = "The door seems to have been locked, but then broken open from the outside. The metal is dented."
        self.keywords = ["broken", "north", "n"]
        self.direction = "north"
        self.location = "central_hallway_west"
        self.destination = "kitchen"
        self.is_open = True
        self.hall_to_kitchen_door = Exit(
            self.label,
            self.name,
            self.description,
            self.location,
            self.keywords,
            self.is_open,
            self.direction,
            self.destination
            )
        self.all_items[self.label] = self.hall_to_kitchen_door
        self.create_exit_reverse("kitchen_to_hall_door", self.hall_to_kitchen_door)
        
    def create_hallway_linker(self):
        self.label = "hallway_linker"
        self.name = "hallway stretching off"
        self.description = "The hallway stretches out to the east. It's dim, but you can see more doors and a looming main portal in the distance."
        self.keywords = ["hall", "east", "e"]
        self.direction = "east"
        self.location = "central_hallway_west"
        self.destination = "central_hallway_east"
        self.is_open = True
        self.hallway_linker = Exit(
            self.label,
            self.name,
            self.description,
            self.location,
            self.keywords,
            self.is_open,
            self.direction,
            self.destination
            )
        self.all_items[self.label] = self.hallway_linker
        self.create_exit_reverse("hallway_linker_reverse", self.hallway_linker)
            
    def create_main_portal(self):
        self.label = "main_portal"
        self.name = "huge set of sliding steel doors, with a card reader nearby"
        self.description = """
This looks like the main entrance to the facility. Two enormous slabs of metal, with
black rubber covering every possible seam. A card reader blinks red beside it.
        """
        self.keywords = ["main", "sliding", "east", "e"]
        self.direction = "east"
        self.location = "central_hallway_east"
        self.destination = "garage"
        self.is_open = False
        self.new_exit = MainPortal(
            self.label,
            self.name,
            self.description,
            self.location,
            self.keywords,
            self.is_open,
            self.direction,
            self.destination
            )
        self.all_items[self.label] = self.new_exit
        self.create_exit_reverse("main_portal_reverse", self.new_exit)
           
        
    def create_scalpel(self):
        #create the scalpel item and add it to the dictionary
        self.scalpel_label = "scalpel"
        self.scalpel_name = "a sharp scalpel"
        self.scalpel_description = "The scalpel is sharp, but flecks of rust-colored blood hint that it's been used."
        self.location = "tube_room"
        self.scalpel_keywords = ["scalpel"]
        self.scalpel_type = "carryable"
        self.scalpel = Item(self.scalpel_label, 
            self.scalpel_name,
            self.scalpel_description,
            self.location,
            self.scalpel_keywords,
            self.scalpel_type
            )
        self.all_items[self.scalpel.label] = self.scalpel
        
    def create_corpse(self):
        #create the corpse item and add it to the dictionary
        self.label = "corpse"
        self.name = "twisted corpse"
        self.description = """
The body is twisted unaturally, but there's no blood, except on his hands.
He is wearing a lab coat.
His pockets are stuffed with energy bars and dried food.
His keycard hangs from a lanyard around his neck.
        """
        self.location = "kitchen"
        self.keywords = ["corpse", "body"]
        self.type = "scenery"
        self.look_special = True
        self.new_item = Item(
            self.label,
            self.name,
            self.description,
            self.location,
            self.keywords,
            self.type,
            self.look_special
            )
        self.all_items[self.label] = self.new_item
       
    def create_keycard(self):
        self.label = "keycard"
        self.name = "keycard"
        self.description = """
        The dead scienctist's keycard.
        """
        self.location = "kitchen"
        self.keywords = ["keycard", "key", "card"]
        self.type = "hidden"
        self.new_item = Item(
            self.label,
            self.name,
            self.description,
            self.location,
            self.keywords,
            self.type
            )
        self.all_items[self.label] = self.new_item
        
    def populator(self):
        #runs each item's creation function and returns the dictionary containing all created items
        self.create_scalpel()
        self.create_corpse()
        self.create_keycard()
        
        #also runs each exit creation function
        self.create_tube_to_hall_doors()
        self.create_hall_to_kitchen_door()
        self.create_hallway_linker()
        self.create_main_portal()
        
        return(self.all_items)
        
    
            
    

class Room(object):
    #common functions for manipulating rooms
    
    def __init__(self, label, verbose_description, terse_description, items, exits):
        #sets up basic room characteristics
        self.label = label
        #internal name of the room, not player-facing
        self.verbose_description = verbose_description
        self.terse_description = terse_description
        self.items = items
        self.exits = exits
        self.visits = 0
        
    def extra_description(self):
        #prints description for each item and exits
        for i, item in self.items.iteritems():
            if item.type != "hidden":
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
        
    def descriptor(self):
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

    
        

class TubeRoom(Room):
    # The starting room. Exits to main hallway.
    #used to set up any special functions needed for the room.
    #currently vestigial from an early organizational attempt
    def placeholder(self, action):
        self.command = action
        if 'door' in self.command:
            print "You go through the doors to the north."
            return('central_hallway_west')
        else:
            print "That doesn't sound like a good idea."
            return('stay')
    
    
    
            
            
class CentralHallwayWest(Room):
    #used to set up any special functions needed for the room.
    #currently vestigial from an early organizational attempt
    def placeholder(self, action):
        self.action = action
        if 'door' in self.action:
            print "You go through the doors to the south."
            return ('tube_room')
        else: 
            print "That doesn't sound like a very good idea."
            return ("stay")
            
class Kitchen(Room):
    #for now, special interactions with a non-movable item are part of the subclass
    #created for each room
    #in the kitchen, the body needs to be searched to find the keycard
    #which, in program terms, means adding the keycard item to the room's dictionary of items
    #after the action command to search the body is given.
    def look_special(self, item_label):        
        self.item_label = item_label
        if self.item_label == "corpse":
            self.items['keycard'].type = "carryable"
        else:
            return "Look special failed" #shouldn't happen
            
class CentralHallwayEast(Room):
    def placeholder(self):
        self.placeholder = "placeholder"
            

        
            
        
class Map(object):
    #creates each room as an instance of the Room class
    #assigns item objects and exit objects to each
    #modular design: each room object created by its own function
    #then setup function runs each room creation function,
    #which creates each room object as an attribute of the map object
    def __init__(self, all_items, player):
        self.all_items = all_items
        self.player = player
        #the vector containing all the items is passed to the map
        #so it can distribute them by calling them out of the dictionary
        self.all_rooms = {}
        #a dictionary that will pair room objects and their labels
        
        
    def exits_setup(self, label):
    #iterates through the item dictionary and makes a new dictionary containing
    #all items designated as exits with the location named in the label variable
    #FUTURE WORK: seems like there should be an easier way to do this
        self.exits = {}
        self.items = {}
        self.label = label
        for key, item in self.all_items.iteritems():
            if item.location == self.label and item.type == "exit":
                self.exits[item.label] = item
            elif item.location == self.label and item.type != "exit":
                self.items[item.label] = item
        return(self.exits, self.items)
        
                
            
    def create_tube_room(self):
        self.label = "tube_room"
        self.tube_room_verbose_description = """The room is lined with large, glass-fronted tubes like the one
you woke up in. The fluorescent lights flicker on and off, buzzing.
In the center of the room is a metal operating table. A cart of
surgical instruments is overturned nearby."""
        self.tube_room_terse_description = "You are in an operating room, lined with mysterious person-sized tubes"
        self.tube_room_exits, self.tube_room_items = self.exits_setup(self.label)
        self.tube_room_visits = 0
        self.tube_room = TubeRoom(
            self.label,
            self.tube_room_verbose_description, 
            self.tube_room_terse_description, 
            self.tube_room_items, 
            self.tube_room_exits
            )
        self.all_rooms[self.label] = self.tube_room
        return(self.tube_room)
    
    def create_central_hallway_west(self):
        self.label = "central_hallway_west"
        self.central_verbose_description = """
The main hallway arcs overhead, and you stand on the western end. The dull thumping of enormous industrial fans
comes from overhead, and their shadows spin crazily on the floor. There's a
wide smear of blood on the grey-green tiles of the floor, starting under one
of the nothern doors and growing gradually thinner as it extends out the main portal
to the east.
"""
        self.central_terse_description = "You are in the western end of the main hallway."
        self.central_exits, self.central_items = self.exits_setup(self.label)
        self.central_visits = 0
        self.central_hallway_west = CentralHallwayWest(
            self.label,
            self.central_verbose_description, 
            self.central_terse_description,
            self.central_items,
            self.central_exits
            )
        self.all_rooms[self.label] = self.central_hallway_west
        return(self.central_hallway_west)
        
    def create_kitchen(self):
        self.label = "kitchen"
        self.verbose_description = """
It seems this was the facility's kitchen. The shelves are lined with empty boxes.
"""
        self.terse_description = "You are in the kitchen."
        self.exits, self.items = self.exits_setup(self.label)
        self.visits = 0
        self.kitchen = Kitchen(
            self.label,
            self.verbose_description, 
            self.terse_description,
            self.items,
            self.exits
            )
        self.all_rooms[self.label] = self.kitchen
        return(self.kitchen)
        
    def create_central_hallway_east(self):
        self.label = "central_hallway_east"
        self.verbose_description = """
You stand in the eastern half of the central hallway. There's a persistent mechanical hum on the
fringes of your hearing. A thick trail of blood begins under the door to the north and leads out
the main portal, growing thinner as it goes."
"""
        self.terse_description = "You are in east half of the main hallway."
        self.exits, self.items = self.exits_setup(self.label)
        self.visits = 0
        self.central_hallway_east = CentralHallwayEast(
            self.label,
            self.verbose_description, 
            self.terse_description,
            self.items,
            self.exits
            )
        self.all_rooms[self.label] = self.central_hallway_east
        return(self.central_hallway_east)
        
    def setup(self):
        #runs each room creation function
        #and creates each room as an attribute of the map
        #also creates and returns a dictionary matching each rooms' label to the room object
        self.tube_room = self.create_tube_room()
        self.central_hallway_west = self.create_central_hallway_west()
        self.central_hallway_east = self.create_central_hallway_east()
        self.kitchen = self.create_kitchen()
        
def debug_init():
    #needed to automate this setup to poke around at
    #internal variables from the interpreter
    #without starting the engine
    #just saves me some typing
    item_setup = ItemsInitializer()
    all_items = item_setup.populator()
    main_map = Map(all_items)
    main_map.setup()
    return(main_map)
    
def mentioned_in(command, items_to_search):
    #to use on both exits and items
    #takes a command (from the user, split into workds) and a dictionary of
    #either exits or items
    #checks to see if the command contains any of the keywords
    #attached to the items in the dictionary
    #if successful, returns the mentioned item
    #if not, returns the string "not_found" (is this a good way to do it?)

    #other ideas: create a null item and return that, so that
    #it always returns the same type

    #other thought: this kind of seems like it conceptually belongs in the parser
    #or as part of the UserCommand class
    #but it needs to happen to room-specific lists of items

    #wow, lots of comments

    #this is rapidly becoming the heart of the program, and i worry that i'm
    #not doing it efficiently. maybe pass only the keys to the item dictionary
    #and return only the needed key, and do the lookup later? but i need to access
    #the keyword list for each item
    
    success = False
    for i, item in items_to_search.iteritems():
        for word in command:
            if word in item.keywords:
                exit_to_try = item
                success = True
    if success == True:
        return(exit_to_try)
    else:
        return("not_found")

    #concern: will just return the last one
    #if same keyword for multiple items
    #and right now only check on that is me assigning the keywords
    #just something to watch for
