import copy
from functools import partial
from game_message import *
#import random
#import math
#import numpy as np
from astar.search import AStar

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def parse_map(self, game_state: TeamGameState) -> AStar:
        return AStar([ [int(tile == TileType.WALL) for tile in row] for row in game_state.map.tiles ])

    def safety(self, action:Action, game_state:TeamGameState)->float:
        safety = []
        pos = self.getFuturePosition(action, game_state)
        for threat in game_state.threats:
            threat_position =(threat.position.x,threat.position.y)
            path = self.map.search(pos[::-1], threat_position[::-1])
            if path is not None:
                safety += [len(path)]
        return min(safety)

    def getFuturePosition(self, action:Action, game_state:TeamGameState):
        my_x = game_state.yourCharacter.position.x
        my_y=game_state.yourCharacter.position.y

        if isinstance(action, MoveLeftAction):
            return (my_x-1,my_y)
        elif isinstance(action, MoveDownAction):
            return (my_x,my_y+1)
        elif isinstance(action,MoveRightAction):
            return (my_x+1,my_y)
        elif isinstance(action,MoveUpAction):
            return (my_x,my_y-1)
    
    def isActionValid(self, action:Action, game_state:TeamGameState):
        x,y = self.getFuturePosition(action,game_state)
        tile = game_state.map.tiles[x][y]
        return tile == TileType.EMPTY

    def print_map(self, game_state: TeamGameState):
        m = copy.deepcopy(self.map.world)
        for i, row in enumerate(m):
            for j, tile in enumerate(row):
                pos = game_state.yourCharacter.position
                row[j] = 'X' if tile else ' '
                if i == pos.y and j == pos.x:
                    row[j] = 'C'
                for threat in game_state.threats:
                    pos = threat.positio
                if i == pos.y and j == pos.x:
                    row[j] = 'V'
        print (*m, sep = "\n")

        
    def get_next_move(self, game_message: TeamGameState):
        self.map = self.parse_map(game_message)
        # self.print_map(game_message)
        # print()

        actions=[
            MoveUpAction(),
            MoveRightAction(),
            MoveDownAction(),
            MoveLeftAction(),
            ]
        actions = [action for action in actions if self.isActionValid(action,game_message)]
        actions = sorted(actions, key =partial(self.safety,game_state =game_message))
        print(actions)
        return [actions[-1]]
