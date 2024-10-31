import copy
from functools import partial
from game_message import *
import random
import math
import numpy as np
from astar.search import AStar

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def parse_map(self, game_state: TeamGameState) -> AStar:
        # Fix: Transpose the map to match x,y coordinates
        return AStar([ [int(tile == TileType.WALL) for tile in row] for row in zip(*game_state.map.tiles) ])

    def safety(self, action:Action, game_state:TeamGameState)->float:
        safety = []
        pos = self.getFuturePosition(action, game_state)
        for threat in game_state.threats:
            threat_position = (threat.position.y, threat.position.x)  # Fix: Swap x,y for AStar
            path = self.map.search(pos, threat_position)  # Fix: Remove [::-1] as we're already passing correct coords
            if path is not None:
                safety += [len(path)]
        return min(safety) if safety else float('inf')  # Fix: Handle case when no paths exist

    def getFuturePosition(self, action:Action, game_state:TeamGameState):
        my_x = game_state.yourCharacter.position.x
        my_y = game_state.yourCharacter.position.y

        if isinstance(action, MoveLeftAction):
            return (my_y, my_x-1)  # Fix: Return (y,x) for AStar
        elif isinstance(action, MoveDownAction):
            return (my_y+1, my_x)  # Fix: Return (y,x) for AStar
        elif isinstance(action, MoveRightAction):
            return (my_y, my_x+1)  # Fix: Return (y,x) for AStar
        elif isinstance(action, MoveUpAction):
            return (my_y-1, my_x)  # Fix: Return (y,x) for AStar
   
    def isActionValid(self, action:Action, game_state:TeamGameState):
        y, x = self.getFuturePosition(action, game_state)  # Fix: Unpack as y,x
        # Fix: Check bounds before accessing tiles
        if (x < 0 or x >= len(game_state.map.tiles) or
            y < 0 or y >= len(game_state.map.tiles[0])):
            return False
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
                    pos = threat.position
                    if i == pos.y and j == pos.x:
                        row[j] = 'V'
        print(*m, sep="\n")

    def get_next_move(self, game_message: TeamGameState):
        self.map = self.parse_map(game_message)
        # self.print_map(game_message)
        # print()

        actions = [
            MoveUpAction(),
            MoveRightAction(),
            MoveDownAction(),
            MoveLeftAction(),
        ]
        actions = [action for action in actions if self.isActionValid(action, game_message)]
        if not actions:  # Fix: Handle case when no valid actions exist
            return []
        actions = sorted(actions, key=partial(self.safety, game_state=game_message))
        return [actions[-1]]