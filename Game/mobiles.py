class Mobile(object):
    #a class for things that move around (currently just the player)
    #tracks inventory and location (Room object)
    
    def __init__(self, inventory, location):
        self.inventory = inventory
        self.location = location
        
        self.new_location = self.location.label
        self.injected = False
        #NOT A ROOM object, just the string matching the label of the new room
        #on start, matches the starting room so player stays in place
        self.victory = False
        
    def move(self, exit):
        #called if the command starts with a movement keyword
        #compares the content of the command to the keywords for
        #each exit in the room
        
        self.exit = exit
        # check to see if the exit is valid/open
        if self.exit.label == 'not_found':
            print "You can't go that way."
        elif self.exit.shall_pass(self):
            print "You go through the %s to the %s.\n" % (self.exit.name, self.exit.direction)
            self.new_location = self.exit.destination
        else:
            print "You can't go that way."
    
    def take(self, item):
        #called if the player is trying to pick something in the room up
        
        self.item = item
        
        if self.item.label == "not_found":
            print "I don't see one of those to pick up.\n"
        elif self.item.type != "carryable":
            print "You can't pick that up.\n"
        else:
            print "You pick up the %s.\n" % self.item.name
            self.inventory.add(self.item)
            del self.location.items[self.item.label]
            
    def drop(self, item):
        #called if the player is trying to drop something
        #reverse of  inventory_take.
        
        self.item = item
        if self.item.label == 'not_found':
            print "You're not carrying one of those.\n"
        else:
            self.inventory.remove(self.item)
            self.location.items[self.item.label] = self.item
                    
            
    def can_see(self):
        #defines the items the mobile can see, for use with the "look" command
        #adds together the items and exits in the room along with inventory items
       
        self.things_to_look_at = dict(self.location.items.items())
        self.things_to_look_at.update(self.location.exits)
        self.things_to_look_at.update(self.inventory.inv_list)
        #and here naming the dict of items "items" gets awkward
        #first line calls the items() property of the dictionary named "items"
        #second line mixes in the exits dictionary
        #this seems awkward but was the best way i could come up with to
        #add multiple dicts while leaving the originals intact
        
        return(self.things_to_look_at)
        
    def look_special(self, item):  
        #allows triggering of events when an item is looked at
        #to add an event to an item, set the item's look_special to True
        #then add the event as an elif branch here
        self.item = item
        
        if self.item.label == 'corpse':
            self.location.items['keycard'].type = "carryable"
        elif self.item.label == 'frozen_corpse':
            self.location.items['key'].type = "scenery"
        elif self.item.label == "fridge":
            self.location.items['syringe'].type = "carryable"
        else:
            print "Look special failed." #shouldn't happen
            
    def use(self, item):
        #called if the parser thinks the player is trying to use an item.
        #calls the appropriate event function for whatever item they're trying to use
        #better way? put flag in the Item object itself?
        self.item = item
        
        if self.item.label == 'scalpel' or (self.location.label == 'garage' and self.item.label=='key'):
            self.cut()
        elif self.item.label == "syringe":
            self.inject()
        elif self.item.label == "core" or (self.location.label == 'reactor' and self.item.label=='key'):
            self.unlock_core()
        elif (self.item.label == 'core' or self.item.label == 'snowmobile'):
            self.fix()
        else:
            self.use_fail()
            
    def use_fail(self):
        print "You don't see how to do that."
        
            
    def cut(self):
        if self.inventory.has('scalpel') == False:
            print "You don't have anything to cut that with."
        elif self.can_cut_key() == False:
            print "Cutting that doesn't seem like it would be a good idea."
        else:
            print "You use the scalpel to cut the key free of the frozen, swollen fingers. The flesh is stiff and bloodless."
            self.location.items['key'].type = "carryable"
 
    def can_cut_key(self):
        if self.location.label != 'garage':
            return False
        elif ('key' in self.location.items.keys()) == False:
            return False
        elif self.location.items['key'].type == 'hidden':
            return False
        else:
            return True
            
    def unlock_core(self):
        if self.inventory.has('key') == False:
            print "You don't have anything that fits in the lock."
        elif self.location.label != 'reactor' or ("core" in self.location.items.keys()) == False:
            print "You don't see anything that key would unlock."
        else:
            print "You put the key into the lock on top of the cylinder and twist. There's a hiss as the top angles open."
            del self.location.items['core']
            self.location.items['open_core'].type = "scenery"
            self.location.items['rod'].type = "carryable"

    def inject(self):
        if self.inventory.has('syringe') == False:
            print "You don't have anything to inject."
        else:
            print "It's clear what you have to do. You grit your teeth and plunge the syringe into your chest. You probably can't really feel the spread of the liquid burning through your arteries, but if feels like you can."
            self.injected = True
            
    def fix(self):
        if self.inventory.has('rod') and self.location.label == 'garage':
            print "You slide the core into the cylinder on the side of the modified snowmobile. It slides into place snugly and the snowmobile's electronics blink to life."
            self.victory = True
        elif self.location.label == 'garage':
            print "The snowmobile is totally inert.  The gas tank and battery have both been removed, and a strange cylindrical assembly mounted on the side. It will need some other power source."
        else:
            print "You really don't think that really needs that kind of power."