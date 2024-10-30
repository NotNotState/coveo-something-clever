from game_message import *
import random
import math

class Bot:
    def __init__(self, train_flag = True):
        self.train_flag = train_flag
        print("Initializing your super mega duper bot")


    def Q(self, current_game_message: TeamGameState):
        return sum ( math.dist(threat.position, current_game_message.yourCharacter.position) for threat in current_game_message.threats )
    
    def delta_Q(self, table_Q, current_Q):

        return 0


    def get_next_move(self, game_message: TeamGameState):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        #make_bot_depressed()
        #return []        

        actions.append(
            random.choice(
                [
                    MoveUpAction(),
                    MoveRightAction(),
                    MoveDownAction(),
                    MoveLeftAction(),
                ]
            )
        )

        # You can clearly do better than the random actions above! Have fun!
        return actions
