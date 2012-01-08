import map
from sys import exit

class Engine(object):
#Takes a map object and an inventory item and manipulates them
    def __init__ (self, map, inventory):
        #sets up recognized keywords.
        self.map = map
        self.movement_keywords = ["go", "n", "e", "s", "w"]
        self.inventory_keywords = dict({"take":"take", "pick":"take", "drop":"drop", "use":"use"})
        self.menu_keywords = ["quit", "help", "i", "inv"]
        self.look_keywords = ["look", "search"]
        
    def move_into(self, room_name):
        #looks up the room with the right label
        #makes the player's location be that room and prints the description
        self.room_name = room_name
        self.room = self.map.all_rooms[self.room_name]
        self.map.player.location = self.room
        self.room.descriptor()
        
    def prompt(self):
        #prints the prompt and returns the input
        print "What do you want to do?"
        action = raw_input("> ")
        return action
   
            
    def menu_commands(self, command):
        #handles straightforward, always-available commands like "quit" and "inv"
        self.command = command
        if "quit" in self.command:
            print "Are you sure? Press Y to quit, any other key to keep playing."
            confirmation = raw_input("> ")
            if confirmation == "Y" or confirmation == "y":
                exit(1)
            else:
                return(False)
        elif command in ['i', 'inv', 'inventory']:
            self.inventory.list()
        else:
            self.parse_fail()
            return(False)
    
    def parse_fail(self):
        #called if the parser doesn't recognize the command
        #can be expanded: multiple rejection phrases
        #this should be called as little as possible in favor of more specific errors
        #in that vein: tracking of commands that get this response so that I can
        #make better resposnes to common unrecognized phrases
        print "I'm afraid I don't know what that means."

    def inventory_parse(self, command):
        #decides whether the command is to take, drop, or use an item and calls the appropriate
        #mobile function.
        self.command = command
        if self.inventory_keywords[self.command[0]] == "take":
            self.map.player.inventory_take(self.command)
        elif self.inventory_keywords[self.command[0]] == "drop":
            self.map.player.inventory_drop(self.command)
        else:
            print "Inventory parsing error" #should never happen
    
    def look_fail(self, command):
        #called when a look command doesn't refer to anything
        #could be made more interesting by referring to the command
        self.command = command
        print "You don't see anything like that."

    def parse(self, action):  
        #breaks commands into categories and then calls an appropriate function
        #there's a lot of dependence on returning "stay" for all commands that don't cause
        #movement, which seems inelegant
        #because i borrowed that central loop from the example game
        #redesign the main loop to stay by default and only change rooms when needed?
        self.action = action
        self.split_command = self.action.split()
        #splits the input into a list of individual words
        self.first_word = self.split_command[0]
        #pulls out the first word, then checks to see if it's in a recognizable category
        #then calls the appropriate function
        if self.first_word in self.menu_keywords:
            self.menu_commands(self.action)
            return()
        elif self.first_word in self.movement_keywords:
            self.map.player.movement(self.split_command)
            return()
        elif self.first_word in self.inventory_keywords:
            self.inventory_parse(self.split_command)
            return()
        elif self.first_word in self.look_keywords:
            self.in_room = self.map.player.look(self.split_command)
            if self.in_room == True:
                return ()
            else:
                self.in_inv = self.map.player.inventory.look(self.split_command)
                if self.in_inv == True:
                    return()
                else:
                    self.look_fail(self.split_command)
                    return()
        else:
            self.parse_fail()
            return ()


items_setup = map.ItemsInitializer()
#creates an instance of the item initializer
all_items = items_setup.populator()
#uses the item initializer to 
#make all_items a dictionary containing all the item objects
inventory = map.Inventory()
#makes an instance of the Inventory class to use as player's inventory
player = map.Mobile(inventory)
#makes an instance of the the Mobile class for the player and puts it in the first room
                
main_map = map.Map(all_items, player)
#makes an instance of the Map class and passes it the item dictionary
main_map.setup()
#runs the setup function in the map object, which creats each room as an attribute of the map
main_engine = Engine(main_map, inventory)
#starts the engine with the map instance
main_map.player.location = main_map.tube_room
main_engine.move_into(main_map.player.location.label)
#sets the player's location to the first room and moves into it

while True:
    action = main_engine.prompt()
    main_engine.parse(action)
    main_engine.move_into(main_map.player.new_location)