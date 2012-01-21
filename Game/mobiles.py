class Mobile(object):
    #a class for things that move around (currently just the player)
    #tracks inventory and location (Room object)
    
    def __init__(self, inventory, location):
        self.inventory = inventory
        self.location = location
        
        self.new_location = self.location.label
        #NOT A ROOM object, just the string matching the label of the new room
        #on start, matches the starting room so player stays in place
        
    def move(self, exit):
        #called if the command starts with a movement keyword
        #compares the content of the command to the keywords for
        #each exit in the room
        
        self.exit = exit
        # check to see if the exit is valid/open
        if self.exit.label == 'not_found':
            print "You can't go that way."
        elif self.exit.shall_pass(self):
            print "You go through the %s to the %s." % (self.exit.name, self.exit.direction)
            self.new_location = self.exit.destination
        else:
            print "You can't go that way."
    
    def take(self, item):
        #called if the player is trying to pick something in the room up
        
        self.item = item
        
        if self.item.label == "not_found":
            print "I don't see one of those to pick up."
        elif self.item.type != "carryable":
            print "You can't pick that up."
        else:
            print "You pick up the %s." % self.item.name
            self.inventory.add(self.item)
            del self.location.items[self.item.label]
            
    def drop(self, item):
        #called if the player is trying to drop something
        #reverse of  inventory_take.
        
        self.item = item
        if self.item.label == 'not_found':
            print "You're not carrying one of those."
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
        else:
            print "Look special failed." #shouldn't happen