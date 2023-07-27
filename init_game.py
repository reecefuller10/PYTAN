import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt


        
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
        player_dict[colours[i]] = player(i, colours[i], {"brick": 0, "wood": 0, "wool": 0, "wheat": 0, 'sheep': 0, 'rock':0}, 15, 5, 4, {"knight": 0, "monopoly": 0, "year_of_plenty": 0, "road_building": 0, "victory_point": 0}, 0)


    return player_dict

def create_bank():

    bank_dict = {"brick": 19, "wood": 19, "sheep": 19, "wheat": 19, 'rock': 19}

    return bank_dict

def create_dev_bank():
  
    dev_bank = ['knight','knight','knight','knight','knight','knight','knight','knight','knight','knight','knight','knight','knight','knight','monopoly','monopoly','year_of_plenty','year_of_plenty','road_building','road_building','victory_point','victory_point','victory_point','victory_point','victory_point']

    return dev_bank

def draw_dev_card(dev_bank, player, player_dict):
    card = random.choice(dev_bank)
    dev_bank.remove(card)

    if card == 'knight':
        player_dict[player].dev_cards['knight'] += 1
    elif card == 'monopoly':
        player_dict[player].dev_cards['monopoly'] += 1
    elif card == 'year_of_plenty':
        player_dict[player].dev_cards['year_of_plenty'] += 1
    elif card == 'road_building':
        player_dict[player].dev_cards['road_building'] += 1
    elif card == 'victory_point':
        player_dict[player].dev_cards['victory_point'] += 1
        
    return card, dev_bank, player_dict

def move_robber(to_tile):

    return to_tile

def give_resource(G, rolls, player_dict,player, terrain_lookup, bank_dict,robber):

    for roll in rolls:
        if roll != robber:
            for node in G.nodes:
                if roll in G.nodes[node]['resource']:
                    if G.nodes[node]['player'] == player:
                        if terrain_lookup[roll] == "desert":
                            print("no resource to give, this is a desert tile")
                        else:
                            #print(player_dict)
                            if G.nodes[node]['city'] == True:
                                player_dict[player].resources[terrain_lookup[roll]] += 2
                                bank_dict[terrain_lookup[roll]] -= 2
                            elif G.nodes[node]['settlement'] == True:
                                player_dict[player].resources[terrain_lookup[roll]] += 1
                                bank_dict[terrain_lookup[roll]] -= 1
        else:
            print("robber is on this tile, no resources given")
                        

    return player_dict, bank_dict

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

def roll_dice(roll_lookup):

    roll = random.randint(1,6)+ random.randint(1,6)

    roll = 8

    print(f'dice rolled a {roll}')

    hexes = [k for k,v in roll_lookup.items() if v == roll]
    
    print(f'hexes giving resources: {hexes}')

    return hexes

def place_settlement(G,player, player_dict, node):

    valid = False
    for n in  G.neighbors(node):
        if G.nodes[n]['settlement'] == True or G.nodes[n]['city'] == True:
            print("You cannot place a settlement here. A settlement is already present on an adjacent node")
            return G, player_dict
    
    for n in G.neighbors(node):
        if G.edges[(node,n)]['player'] == player:
            print(f'there is a road from {node} to {n}, therefore valid')
            valid = True

    if valid:
        if player_dict[player].settlements > 0:
            G.nodes[node]['player'] = player
            G.nodes[node]['settlement'] = True
            player_dict[player].settlements -= 1

        else:
            print("You do not have any settlements left to place")
    else:
        print(f'no road adjacent to {node}')

    return G, player_dict

def place_city(G,player, player_dict, node):
        
        valid = False
        for n in  G.neighbors(node):
            if G.nodes[n]['settlement'] == True or G.nodes[n]['city'] == True:
                print("You cannot place a settlement here. A settlement is already present on an adjacent node")
                return G, player_dict
        
        for n in G.neighbors(node):
            if G.edges[(node,n)]['player'] == player:
                print(f'there is a road from {node} to {n}, therefore valid')
                valid = True
        
        if valid:
            if player_dict[player].cities > 0:
                G.nodes[node]['player'] = player
                G.nodes[node]['city'] = True
                player_dict[player].cities -= 1
        
            else:
                print("You do not have any cities left to place")
        else:
            print(f'no road adjacent to {node}')

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

    G.add_nodes_from([i for i in range(30)], type='vertex', player = None, settlement = False, city = False, robber = False)
        
    for i in G.nodes:
        if i != 29:
            G.add_edge(i, i+1)
        else:
            G.add_edge(i, 0)
    
    G.add_nodes_from([i for i in range(30,48)],type = 'vertex', player = None,settlement = False, city = False, robber = False)

    for i in range(30,48):
        if i != 47:
            G.add_edge(i, i+1)
        else:
            G.add_edge(i, 30)

    G.add_nodes_from([i for i in range(48, 54)], type = 'vertex', player = None,settlement = False, city = False, robber = False)

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

    terrain = ["wood", "wood", "wood", "wood", "sheep", "sheep", "sheep", "sheep", "wheat", "wheat", "wheat", "wheat", "brick", "brick", "brick", "rock", "rock", "rock", "desert"]
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

    dev_bank = create_dev_bank()

    terrain_lookup = populate_terrain()
    x = [k for k,v in terrain_lookup.items() if v == "desert"]
    print(f'desert: {x}')

    robber = x[0]

    print(f'robber: {robber}')

    bank_dict = create_bank()

    roll_lookup = create_roll_prob(G, terrain_lookup)

    player_dict = create_players(4)
    
    roll_dice(roll_lookup)

    print(player_dict['red'].settlements)

    print(G.nodes[0]['player'])
    print(G.nodes[0]['settlement'])

    print(G.edges[(0,1)]['player'])

    G, player_dict = place_road(G, "red", player_dict, (0,1))

    print(G.edges[(0,1)]['player'])

    print(f'red resources {player_dict["red"].resources}')
    print(f'blue resources {player_dict["blue"].resources}')

    G, player_dict = place_road(G, "red", player_dict, (8,9))
    G, player_dict = place_settlement(G, "red", player_dict, 9)
    G, player_dict = place_road(G, "red", player_dict, (38,11))
    G, player_dict = place_city(G, "red", player_dict, 38)
    G, player_dict = place_settlement(G, "blue", player_dict, 45)
    G, player_dict = place_settlement(G, "red", player_dict, 44)
    print(f'placed settlements for red on nodes 0 and 1')
    print(f'placed settlements for blue on nodes 45')
    
    roll = roll_dice(roll_lookup)

    
    
    player_dict, bank_dict = give_resource(G, roll, player_dict, "red", terrain_lookup, bank_dict,robber)
    player_dict, bank_dict = give_resource(G, roll, player_dict, "blue", terrain_lookup, bank_dict,robber)
    player_dict, bank_dict = give_resource(G, roll, player_dict, "green", terrain_lookup, bank_dict,robber)
    player_dict, bank_dict = give_resource(G, roll, player_dict, "yellow", terrain_lookup, bank_dict,robber)

    print(f'red resources {player_dict["red"].resources}')
    print(f'blue resources {player_dict["blue"].resources}')
    print(f'green resources {player_dict["green"].resources}')
    

    nx.draw(G, with_labels=True, font_weight='bold')

    #plt.show()
    

if __name__ == "__main__":
    main()