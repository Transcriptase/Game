import items
import exits
import inventory
import mobiles
import rooms
        
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
      
    def setup(self):
        all_items = items.populate()
        all_exits = exits.populate
        
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
