from sys import exit

class Engine(object):
#Parses player commands and manipulates a map object
    def __init__ (self, map, player):
        #sets up recognized keywords.
        self.map = map
        self.player = player
        
        self.movement_keywords = [
            "go",
            "n",
            "e",
            "s",
            "w",
            "north",
            "east",
            "south",
            "west"]
        self.inventory_keywords = dict({
            "take":"take",
            "pick":"take",
            "drop":"drop",
        })
        self.menu_keywords = ["quit", "help", "i", "inv"]
        self.look_keywords = ["look", "search", "read"]
        
    def move_into(self, room_name):
        #looks up the room with the right label
        #makes the player's location be that room and prints the description
        self.room_name = room_name
        self.room = self.map.all_rooms[self.room_name]
        self.player.location = self.room
        self.room.describe()
        
    def prompt(self):
        #prints the prompt and returns the input
        print "\nWhat do you want to do?"
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
            self.player.inventory.list()
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
            self.item_to_try = self.mentioned_in(self.command, self.player.location.items)
            self.player.take(self.item_to_try)
        elif self.inventory_keywords[self.command[0]] == "drop":
            self.item_to_try = self.mentioned_in(self.command, self.player.inventory.inv_list)
            self.player.drop(self.item_to_try)
        else:
            print "Inventory parsing error" #should never happen
            
    
    def look_fail(self, command):
        #called when a look command doesn't refer to anything
        #could be made more interesting by referring to the command
        self.command = command
        print "You don't see anything like that."

    def parse(self, action):  
        #breaks commands into categories and then calls an appropriate function
               
        self.action = action
        self.split_command = self.action.split()
        #splits the input into a list of individual words
        self.first_word = self.split_command[0]
        #pulls out the first word, then checks to see if it's in a recognizable category
        #then calls the appropriate function
        
        if self.first_word in self.menu_keywords:
            self.menu_commands(self.action)
        elif self.first_word in self.movement_keywords:
            self.exit_to_try = self.move_parse(self.split_command)
        elif self.first_word in self.inventory_keywords:
            self.inventory_parse(self.split_command)
        elif self.first_word in self.look_keywords:
            self.look_parse(self.split_command)
        #that was the easy part, since they use predictable verbs        
        
        else:
            self.use_words = self.use_words_lookup()
            if self.first_word in self.use_words:
                self.use_parse(self.split_command)
            else:
                self.parse_fail()
                
    def use_words_lookup(self):
        self.use_words = ['use']
        for label, item in self.player.can_see().iteritems():
            if item.use_words != "":
                for word in item.use_words:
                    self.use_words.append(word)
        return(self.use_words)
            
            
    def look_parse(self, command):
        self.command = command
        
        if len(self.command) == 1:
            #single-word phrases that trigger the look parser, like "look"
            #and "search" will print the location's full description
            self.player.location.describe_verbose()
            
        else:
            self.looked_at = self.mentioned_in(self.command, self.player.can_see())
        
            if self.looked_at.label != 'not_found':
                print self.looked_at.description
            else:
                self.look_fail()
            
            if self.looked_at.look_special == 'yes':
                self.player.look_special(self.looked_at)
            
       
    def move_parse(self, command):
        self.command = command
        self.exit_to_try = self.mentioned_in(self.command, self.player.location.exits)
        self.player.move(self.exit_to_try)
        self.move_into(self.player.new_location)
            
    def look_fail(self):
        print "You don't see anything like that here."
        
    def use_parse(self, command):
        #this is triggered if the command starts with a possible use word
        self.command = command
        
        self.use_item = self.mentioned_in(self.command, self.player.can_see())
        if self.use_item.label == "not_found":
            self.use_fail()
        else:
            self.player.use(self.use_item)
            
    def use_fail(self):
        print "You don't see any way to do that."
            
    def mentioned_in(self, command, items_to_search):
    #to use on both exits and items
    #takes a command (from the user, split into workds) and a dictionary of
    #either exits or items
    #checks to see if the command contains any of the keywords
    #attached to the items in the dictionary
    #if successful, returns the mentioned item
    #if not, returns the dummy item "not_found"
        
        self.command = command
        self.items_to_search = items_to_search
        self.success = False
        
        for i, item in self.items_to_search.iteritems():
            for word in self.command:
                if word in item.keywords:
                    self.exit_to_try = item
                    self.success = True
        if self.success == True:
            return(self.exit_to_try)
        else:
            return(self.map.all_exits["not_found"])
            
    def simulate_play(self, command_list):
    #for debugging purposes, takes a list of commands and parses them in order
        self.command_list = command_list
        for command in self.command_list:
            self.parse(command)
    
    def victory(self):
        print "With a touch of the ignition button, the snowmobile roars with way more power than it needs. You climb on and steer it out into the blinding snow, hoping you will reach civilization while you can still be described as civilized."
        print "Congratulations! You are a winner!"
        exit(1)