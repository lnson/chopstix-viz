import copy
from enum import Enum

from absl import app, flags
from graphviz import Digraph

FLAGS = flags.FLAGS

flags.DEFINE_integer('num_hands', 2, 'Number of hands.')
flags.DEFINE_integer('num_fingers', 4, 'Number of fingers on each hand.')
flags.DEFINE_string('output_file', 'game-state.pdf',
                    'Name of output state machine file.')


class Turn(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2

    def next(self):
        if self == Turn.PLAYER_1:
            return Turn.PLAYER_2
        return Turn.PLAYER_1


class Player:
    def __init__(self, numHands: int, numFingers: int):
        self.hands = [1] * numHands
        self.numFingers = numFingers

    def __eq__(self, other):
        return self.hands == other.hands

    def __hash__(self):
        return hash(tuple(self.hands))

    def __str__(self):
        return ','.join(str(hand) for hand in self.hands)

    def addToHand(self, whichHand: int, fingersToAdd: int):
        if len(self.hands) == 0:
            return

        self.hands[whichHand] = (
            self.hands[whichHand] + fingersToAdd) % self.numFingers
        self.hands = sorted(self.hands)

        idx = 0
        while idx < len(self.hands) and self.hands[idx] == 0:
            idx += 1

        self.hands = self.hands[idx:]

    def getHands(self):
        return self.hands


class GameState:
    def __init__(self, player1: Player, player2: Player, turn: Turn):
        self.player1 = player1
        self.player2 = player2
        self.turn = turn

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        turnIndicator = '>>'
        if self.turn == Turn.PLAYER_2:
            turnIndicator = '<<'
        return "({0}{1}{2})".format(self.player1, turnIndicator, self.player2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        return self.turn == other.turn and self.player1 == other.player1 and self.player2 == other.player2

    def __hash__(self):
        return hash(self.player1) + hash(self.player2) + hash(self.turn)

    def nextStates(self):
        result = set()
        if len(self.player1.getHands()) == 0:
            return result
        if len(self.player2.getHands()) == 0:
            return result

        if self.turn == Turn.PLAYER_1:
            for numFingers in self.player1.getHands():
                for fingerIdx in range(len(self.player2.getHands())):
                    newPlayer2 = copy.deepcopy(self.player2)
                    newPlayer2.addToHand(fingerIdx, numFingers)
                    result.add(
                        GameState(self.player1, newPlayer2, self.turn.next()))
        else:
            for numFingers in self.player2.getHands():
                for fingerIdx in range(len(self.player1.getHands())):
                    newPlayer1 = copy.deepcopy(self.player1)
                    newPlayer1.addToHand(fingerIdx, numFingers)
                    result.add(
                        GameState(newPlayer1, self.player2, self.turn.next()))

        return result

    def player1Wins(self):
        return len(self.player2.getHands()) == 0

    def player2Wins(self):
        return len(self.player1.getHands()) == 0


def addStateToGraph(state: GameState, graph: Digraph):
    color = 'black'
    if state.player1Wins():
        color = 'green'
    elif state.player2Wins():
        color = 'red'
    graph.node(str(state), color=color)


def linkStates(srcState: GameState, destState: GameState, graph: Digraph):
    graph.edge(str(srcState), str(destState))


def graphStates(numHands: int, numFingers: int):
    graph = Digraph()
    p1 = Player(numHands, numFingers)
    p2 = Player(numHands, numFingers)

    state = GameState(p1, p2, Turn.PLAYER_1)
    # Nodes that were visited.
    visited = set()
    # Nodes that were encountered while BFS-ing, not necessarily visited.
    encountered = set(visited)
    # Nodes to be visited.
    toBeVisited = [state]

    while len(toBeVisited) != 0:
        state = toBeVisited.pop()
        visited.add(state)
        addStateToGraph(state, graph)

        for nextState in state.nextStates():
            if nextState not in encountered:
                addStateToGraph(nextState, graph)
                encountered.add(nextState)
                toBeVisited.append(nextState)
            linkStates(state, nextState, graph)

    return graph


def main(argv):
    graphStates(FLAGS.num_hands, FLAGS.num_fingers).render(
        FLAGS.output_file, view=True)


if __name__ == '__main__':
    app.run(main)
