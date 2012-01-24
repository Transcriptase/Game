class Inventory(object):
    #manages the player's inventory
    #creates a dictionary using an item's label as the key
    #linked to the Item-class object
    
    def __init__(self):
        self.inv_list = {}
        
    def add(self, item):
        self.item = item
        if self.has(self.item):
            self.add_error(self.item)
        else:
            self.inv_list[self.item.label] = self.item
        
    def remove(self, item):
        self.item = item
        if self.has(self.item.label):
            del self.inv_list[self.item.label]
        else:
            self.remove_error(self.item)
        
    def has(self, label):
        self.label = label
        if self.label in self.inv_list.keys():
            return True
        else:
            return False
            
    def describe(self, item):
        self.item = item
        if self.has(self.item.label):
            print self.item.description
        else:
            print "You are not carrying a %s.\n" % self.item.name
        
    def list(self):
    #lists the contents of the inventory
        if self.inv_list == {}:
            print "You are not carrying anything."
        else:
            print "You are carrying:\n"
        for i, item in self.inv_list.iteritems():
            print item.name
            
#these should probably never happen because of how add and remove are called
#as part of mobile.take/drop, which should only be called in pre-screened circumstances

    def remove_error(self, item):
        print "%s not found in inventory." % self.item.label
        
    def add_error(self, item):
        print "%s already in inventory" % self.item.label