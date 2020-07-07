from graphviz import Digraph
from collections import deque


Epsilon = 'Epsilon'

class State:

    def __init__(self, isEnd = False):
        self.isEnd = isEnd
        self.next = {}

    def addNext(self, token, to):
        # print(self.next, token, to)
        if token not in self.next: 
            self.next[token] = []
        self.next[token].append(to)

class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end= end
    
    @staticmethod
    def _initState():
        return State(), State(True)

    @staticmethod
    def BASIC(token):
        start, end = NFA._initState()
        start.addNext(token, end) # S -- token --> E
        return NFA(start, end)

    @staticmethod
    def OR(nfa1, nfa2):
        start, end = NFA._initState()
        
        start.addNext(Epsilon, nfa1.start) # S -- e --> NFA1
        start.addNext(Epsilon, nfa2.start) # S -- e --> NFA2
        nfa1.end.addNext(Epsilon, end)  # NFA1 -- e --> E
        nfa2.end.addNext(Epsilon, end)  # NFA2 -- e --> E

        nfa1.end.isEnd, nfa2.end.isEnd = False, False
        return NFA(start, end)
    
    @staticmethod
    def CONCAT(nfa1, nfa2):
        start, end = NFA._initState()
        
        start.addNext(Epsilon, nfa1.start) # E -- e --> NFA1
        nfa1.end.addNext(Epsilon, nfa2.start) # NFA1 -- e --> NFA2
        nfa2.end.addNext(Epsilon, end) # NFA2 -- e --> NFA1

        nfa1.end.isEnd = False
        nfa2.end.isEnd = False

        return NFA(start, end)

    @staticmethod
    def CLOSURE(nfa):
        start, end = NFA._initState()
        start.addNext(Epsilon,nfa.start) # S -- e --> NFA
        nfa.end.addNext(Epsilon,end) # NFA -- e --> NFA
        end.addNext(Epsilon, start) # E -- e --> S

        nfa.end.isEnd = False
        return NFA(start, end)

    def toGraph(self):
        dot = Digraph(name='nfa', format="png")
        dot.attr(rankdir='LR')
        state2index = {}
        q = deque()
        q.append(self.start)
        g = []

        while len(q):
            state = q.popleft()
            if state in state2index:
                continue
            state2index[state] = 'State' + str(len(state2index))
            index = state2index[state]
            dot.node(name = index, label=index, shape= 'doublecircle' if state.isEnd else 'circle')
            for token, states in state.next.items():
                for nextState in states:
                    g.append((state, token, nextState))
                    q.append(nextState)

        # output
        for start, token, end in g:
            startIndex, endIndex = state2index[start], state2index[end]
            print('{} -- {} --> {}'.format(startIndex, token, endIndex))
            dot.edge(startIndex, endIndex, label=token)

        dot.node(name='start', label='S', shape="plaintext")
        dot.edge('start', state2index[self.start])

        dot.render(filename='nfa', directory='./')
        return state2index
	
    def geneState2Index(self):
        state2index = {}
        q = deque()
        q.append(self.start)

        while len(q):
            state = q.popleft()
            if state in state2index:
                continue
            state2index[state] = 'State' + str(len(state2index))
            index = state2index[state]
            for token, states in state.next.items():
                for nextState in states:
                    q.append(nextState)

        return state2index
        
	
    def GetEpsilonClosure(states):
        visited = set(states)
        q = deque(states)
        while len(q):
            state = q.popleft()
            for item in state.next.get(Epsilon, []):
                if item not in visited:
                    q.append(item)
                    visited.add(item)
        return visited

    def match(self, s):
        states = set([self.start])
        for c in s:
            # Epsilon ->
            states = NFA.GetEpsilonClosure(states)
            nextStates = set()
            for state in states:
                for nextState in state.next.get(c, []):
                    nextStates.add(nextState)
            states = nextStates
            if len(states) == 0:
                break
        states = NFA.GetEpsilonClosure(states)
        for state in states:
            if state.isEnd:
                return True
        return False