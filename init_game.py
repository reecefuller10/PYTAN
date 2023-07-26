import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

class resource:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount

# resources and dev cards should be dictionaries
class player:
    def __init__(self, ID, color, resources, roads, settlements, cities, dev_cards, victory_points):
        self.ID = ID
        self.color = color
        self.resources = resources
        self.roads = roads
        self.settlements = settlements
        self.cities = cities
        self.dev_cards = dev_cards
        self.victory_points = victory_points

def create_players(num):
    player_list = []
    colours = ["red", "blue", "green", "yellow"]
    player_dict = {}
    for i in range(num):
        player_dict[colours[i]] = player(i, colours[i], {"bricks": 0, "lumber": 0, "wool": 0, "wheat": 0}, 15, 5, 4, {"knight": 0, "monopoly": 0, "year_of_plenty": 0, "road_building": 0, "victory_point": 0}, 0)

    print(player_dict)
    return player_dict

def create_bank():

    bricks = resource("bricks", 19)
    lumber = resource("lumber", 19)
    wool = resource("wool", 19)
    wheat= resource("wheat", 19)

    bank_dict = {"bricks": bricks, "lumber": lumber, "wool": wool, "wheat": wheat}

    return bank_dict

def give_resource(player, resource, amount, bank_dict):
    player.resources[resource] += amount
    bank_dict[resource].amount -= amount

    return player, bank_dict

def trade(player1, player2, resource1, resource2, amount1, amount2):
    player1.resources[resource1] -= amount1
    player1.resources[resource2] += amount2
    player2.resources[resource1] += amount1
    player2.resources[resource2] -= amount2

    return player1, player2

def link_resource_tiles(G):

    zero = [0,1,29,30,31,32]
    one = [1,2,3,4,32,33]
    two = [4,5,6,33,34,35]
    three = [6,7,8,9,35,36]
    four = [9,10,11,36,37,38]
    five = [11,12,13,14,38,39]
    six = [14,15,16,39,40,41]
    seven = [16,17,18,19,41,42]
    eight = [19,20,21,42,43,44]
    nine = [21,22,23,24,44,45]
    ten = [24,25,26,45,46,47]
    eleven = [26,27,28,29,47,30]
    twelve = [30,31,46,47,48,53]
    thirteen = [31,32,33,34,48,49]
    fourteen = [34,35,36,37,49,50]
    fifteen = [37,38,39,40,50,51]
    sixteen = [40,41,42,43,51,52]
    seventeen = [43,44,45,46,52,53]
    eighteen = [48,49,50,51,52,53]

    for node in G.nodes:
        G.nodes[node]['resource'] = []
    

    resource_list = [zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen]

    for i in range (0,19): #i is the ID of a resource tile, must tie it to the correct node(s)
        for j in resource_list[i]:
            G.nodes[j]['resource'].append(i)
    
    #G.nodes[node]['resource'] to access a list showing which resources are adjacent to a node 
    

    return G

def roll_dice(G, player_dict, bank_dict, roll_lookup):

    roll = random.randint(1,6)+ random.randint(1,6)
    print(f'roll: {roll}')

    x = [k for k,v in roll_lookup.items() if v == roll]

    print(f'hexes giving resources: {x}')

def place_settlement(G,player, player_dict, node):

    if player_dict[player].settlements > 0:
        G.nodes[node]['player'] = player
        G.nodes[node]['settlement'] = True
        player_dict[player].settlements -= 1

    else:
        print("You do not have any settlements left to place")

    return G, player_dict
    
def place_road(G,player,player_dict,edge):

    if player_dict[player].roads > 0:
        G.edges[edge]['player'] = player
        player_dict[player].roads -= 1

    else:
        print("You do not have any roads left to place")

    return G, player_dict


def create_roll_prob(G, terrain_lookup):

    rolls = [5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]

    desert_tile = list(terrain_lookup.keys())[list(terrain_lookup.values()).index("desert")]

    #print(desert_tile)

    roll_lookup = {}

    for i in range(0,18):
        if i != desert_tile:
            roll_lookup[i] = rolls[i]

    print(f'roll_lookup: {roll_lookup}')

    x = [k for k,v in roll_lookup.items() if v == 12]

    
    #print(f'x: {x}')


    return roll_lookup


def create_4_player_board():
    G = nx.Graph()
    G.add_nodes_from([i for i in range(30)], type='vertex', player = None, settlement = False, city = False)
        
    for i in G.nodes:
        if i != 29:
            G.add_edge(i, i+1)
        else:
            G.add_edge(i, 0)
    
    G.add_nodes_from([i for i in range(30,48)],type = 'vertex', player = None,settlement = False, city = False)

    for i in range(30,48):
        if i != 47:
            G.add_edge(i, i+1)
        else:
            G.add_edge(i, 30)

    G.add_nodes_from([i for i in range(48, 54)], type = 'vertex', player = None,settlement = False, city = False)

    for i in range(48,54):
        if i != 53:
            G.add_edge(i, i+1)
        else:
            G.add_edge(i, 48)
    
    from_node = 1
    to_node = 32
    #odd true -> add 3 to from_node, 1 to to_node
    #odd false -> add 2 to from_node, 2 to to_node
    odd = True

    for i in range(0,12):
        
        G.add_edge(from_node, to_node)
        if odd:
            from_node += 3
            to_node += 1
            odd = False
        else:
            from_node += 2
            to_node += 2
            odd = True
        if to_node == 47:
            G.add_edge(from_node, to_node)
            from_node = 29
            to_node = 30
            G.add_edge(from_node, to_node)
            break

    to_node = 48
    from_node = 31
    for i in range(0,6):
        G.add_edge(from_node, to_node)
        from_node += 3
        to_node += 1
        if to_node == 53:
            break

    

        
    G = link_resource_tiles(G)

    for edge in G.edges:
        G.edges[edge]['player'] = None
        
    return G

def populate_terrain():

    terrain = ["forest", "forest", "forest", "forest", "pasture", "pasture", "pasture", "pasture", "field", "field", "field", "field", "hill", "hill", "hill", "mountain", "mountain", "mountain", "desert"]
    terrain_lookup = {}

    is_random = True

    if is_random == True:
        for i in range(0,19):
            hex = random.choice(terrain)
            terrain.remove(hex)
            terrain_lookup[i] = hex
    else:
        for i in range(0,19):
            terrain_lookup[i] = terrain[i]

    return terrain_lookup

def get_resource():
    pass


def main():

    
    G = create_4_player_board()

    print(G.nodes.data())

    terrain_lookup = populate_terrain()
    print(terrain_lookup)

    bank_dict = create_bank()

    roll_lookup = create_roll_prob(G, terrain_lookup)

    player_dict = create_players(4)
    
    roll_dice(G,player_dict,bank_dict, roll_lookup)

    print(G.nodes(data=True))

    print(player_dict['red'].settlements)

    print(G.nodes[0]['player'])
    print(G.nodes[0]['settlement'])

    G, player_dict = place_settlement(G, "red", player_dict, 0)

    print(player_dict['red'].settlements)

    print(G.nodes[0]['player'])
    print(G.nodes[0]['settlement'])

    print(G.edges[(0,1)]['player'])

    G, player_dict = place_road(G, "red", player_dict, (0,1))

    print(G.edges[(0,1)]['player'])

    nx.draw(G)

    plt.show()
    

if __name__ == "__main__":
    main()