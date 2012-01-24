from nose.tools import *
import Game.items
import Game.exits
import Game.inventory
import Game.mobiles
import Game.rooms
import Game.map
import Game.engine

def setup():
    test_inv = Game.inventory.Inventory()
    test_map = Game.map.Map()
    test_map.setup()
    test_player = Game.mobiles.Mobile(test_inv, test_map.all_rooms['tube_room'])
    test_engine = Game.engine.Engine(test_map, test_player)
    return(test_engine)

def test_item_setup():
    all_items = Game.items.populate()
    
    assert_equal(all_items['keycard'].name, 'keycard')
    assert_equal(all_items['corpse'].location, 'kitchen')
    assert_equal(all_items['scalpel'].type, 'carryable')
    
def test_exit_setup():
    engine = setup()
    
    assert_equal(engine.map.all_exits['tube_to_hall'].destination, 'central_hallway_west')
    assert_equal(engine.map.all_exits['tube_to_hall_rev'].destination, 'tube_room')
    assert_equal('s' in engine.map.all_exits['tube_to_hall_rev'].keywords, True)
    assert_equal('south' in engine.map.all_exits['tube_to_hall_rev'].keywords, True)
    assert_equal(engine.map.all_exits['main_portal'].is_open, False)
    
    
def test_inventory_setup():
    all_items = Game.items.populate()
    test_inv = Game.inventory.Inventory()
    test_item = all_items['scalpel']
    
    test_inv.add(test_item)
    
    assert_equal(len(test_inv.inv_list), 1)
    assert_equal(test_inv.has(test_item.label), True)
    
    test_inv.remove(test_item)
    
    assert_equal(len(test_inv.inv_list), 0)
    
def test_room_setup():
    all_rooms = Game.rooms.populate()
    
    assert_equal(all_rooms['tube_room'].terse_description, "You are in an operating room, lined with mysterious person-sized tubes")
    
def test_map_setup():
    engine = setup()
    
    assert_equal(engine.map.all_rooms['kitchen'].items['corpse'].type, 'scenery')
    
    
def test_mobile():
    engine  = setup()
    player = engine.player
    item = engine.map.all_items['scalpel']
    exit = engine.map.all_exits['tube_to_hall']
    
    player.take(item)
    assert_equal(len(player.inventory.inv_list), 1)
    
    player.move(exit)
    assert_equal(player.new_location, 'central_hallway_west')
    
    player.location = engine.map.all_rooms['kitchen']
    player.look_special(player.location.items['corpse'])
    
    assert_equal(player.location.items['keycard'].type, "carryable")
    
    player.location = engine.map.all_rooms['garage']
    
    assert_equal(player.location.items['key'].type, "hidden")
    
    player.look_special(player.location.items['frozen_corpse'])
    
    assert_equal(player.location.items['key'].type, "scenery")
    
    player.cut()
    
    assert_equal(player.location.items['key'].type, "carryable")
    
    player.inventory.add(engine.map.all_items['syringe'])
    player.inject()
    
    assert_equal(player.injected, True)
    
    player.location = engine.map.all_rooms['garage']
    player.inventory.add(engine.map.all_items['rod'])
    
    player.fix()
    
    assert_equal(player.victory, True)
    
    
    
def test_engine():
    engine = setup()
    
    pickup_sequence = [
        'dance', # nonsense command
        'look shoe', #look for non existent item
        'look scalpel', #look for real item
        'take shoe', #take non existent item
        'take scalpel', #take real item
        'inv' #list inventory
        ]
    
    engine.simulate_play(pickup_sequence)
        
    assert_equal(engine.player.inventory.has('scalpel'), True)
    assert_equal(len(engine.player.location.items), 0)
    assert_equal(engine.player.location.label, 'tube_room')
    # scalpel is picked up and no longer present in room
    
    move_and_drop = [
        'n', #move to west hall using short command
        'drop scalpel',
        'go south', # move back to tube room using full command
        'go north' # back to hall
        ]

    engine.simulate_play(move_and_drop)
    
    assert_equal(engine.player.location.label, 'central_hallway_west')
    assert_equal('scalpel' in engine.player.location.items.keys(), True)
    assert_equal(len(engine.player.inventory.inv_list), 0)
    
    #player is in west hall and has dropped scalpel
    
    dead_end = [
        'take scalpel', #pick scalpel back up for cut test
        'e', #move to east hall
        'e', #try main portal
        'go east' #try main portal again
        ]
    
    engine.simulate_play(dead_end)
    
    assert_equal(engine.player.location.label, 'central_hallway_east')
    #player is still in east hall despite three east commands
    
    find_keycard = [
        'w', #move to west hall
        'go north', #move to kitchen
        'look corpse', #unhide keycard
        'take keycard'
        ]
    
    engine.simulate_play(find_keycard)
    
    assert_equal(engine.player.location.label, 'kitchen')
    assert_equal(engine.player.inventory.has('keycard'), True)
    #player is in kitchen holding keycard
    
    find_parka = [
        's', #move to west hall
        'e', #move to east hall
        's', #move to closet
        'take parka' #pick up parka
        ]
    engine.simulate_play(find_parka)
    assert_equal(engine.player.location.label, 'closet')
    assert_equal(engine.player.inventory.has('parka'), True)
    
    open_main = [
        'n', #move to east hall
        'e' #go out main portal
        ]
        
    engine.simulate_play(open_main)
    assert_equal(engine.player.location.label, 'outside')
    
    find_key = [
        's', #go to garage
        'look body', #reveal keycard
        "take key" #fails
        ]
    engine.simulate_play(find_key)
    
    assert_equal(engine.player.location.label, 'garage')
    assert_equal('key' in engine.player.location.items.keys(), True)
    assert_equal(engine.player.location.items['key'].type, 'scenery')
    #player is in garage, key is visible but can't be taken
    
    cut_key = [
        'cut key', #cuts the key out
        'take key' #takes key
        ]
        
    engine.simulate_play(cut_key)
    
    assert_equal(engine.player.inventory.has('key'), True)
    
    inject = [
        'n', #leave garage
        'w', #back to east hall
        'n', #into lab
        'look fridge', #reveal syringe
        'take syringe',
        'inject self'
        ]
        
    engine.simulate_play(inject)
    
    assert_equal(engine.player.location.label, 'lab')
    assert_equal(engine.player.inventory.has('syringe'), True)
    assert_equal(engine.player.injected, True)
    
    get_core = [
        's', #to east hall
        'w', #to west hall
        'w', # down stairs
        's', # into reactor
        'unlock cylinder', #open core
        'take rod'
        ]
        
    engine.simulate_play(get_core)
    
    assert_equal(engine.player.location.label, 'reactor')
    assert_equal(engine.player.inventory.has('rod'), True)
    
    fix = [
        'n', #to reactor foyer
        'e', #to west hall
        'e', #to east hall
        'e', #outside
        's', #to garage
        'fix snowmobile' #fix snowmobile
        ]
        
    engine.simulate_play(fix)
    
    assert_equal(engine.player.location.label, 'garage')
    assert_equal(engine.player.victory, True)

def prepare_fix():
    #I'm breaking this out into its own function so I can poke with
    #the interpreter more easily if I have to.
    eng = setup()
    eng.player.location = eng.map.all_rooms['garage']
    eng.player.inventory.add(eng.map.all_items['rod'])
    return eng
    
def test_fix():
    eng = prepare_fix()
    eng.parse('use snowmobile')
    
    assert_equal(eng.player.victory, True)
    
