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
    all_exits = Game.exits.populate()
    
    assert_equal(all_exits['tube_to_hall'].destination, 'central_hallway_west')
    assert_equal(all_exits['tube_to_hall_rev'].destination, 'tube_room')
    assert_equal('s' in all_exits['tube_to_hall_rev'].keywords, True)
    assert_equal('south' in all_exits['tube_to_hall_rev'].keywords, True)
    assert_equal(all_exits['main_portal'].is_open, False)
    
    config_list = Game.exits.create_config_list()
    config = config_list[0]
    reversed_config = Game.exits.create_config_reverse(config)
    assert_equal('central_hallway_west', reversed_config['location'])
    assert_equal('tube_room', reversed_config['destination'])

    
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
        'e', #move to east hall
        'e', #try main portal
        'go east' #try main portal again
        ]
    
    engine.simulate_play(dead_end)
    
    assert_equal(engine.player.location.label, 'central_hallway_east')
    #player is still in east hall despite three east commands
    
    find_key = [
        'w', #move to west hall
        'go north', #move to kitchen
        'look corpse', #unhide keycard
        'take keycard'
        ]
    
    engine.simulate_play(find_key)
    
    assert_equal(engine.player.location.label, 'kitchen')
    assert_equal(engine.player.inventory.has('keycard'), True)
    #player is in kitchen holding keycard
    

