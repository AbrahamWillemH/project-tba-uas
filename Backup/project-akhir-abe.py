from transitions import transitions

class TM_Multitape:
    def __init__(self, num_tapes, initial_state, accepting_states, transitions):
        self.num_tapes = num_tapes
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.reset()
    
    def reset(self):
        self.tapes = [[' '] for _ in range(self.num_tapes)]
        self.heads = [0] * self.num_tapes
        self.state = self.initial_state

    def step(self):
        current_symbols = tuple(self.tapes[i][self.heads[i]] for i in range(self.num_tapes))
        action = self.transitions.get((self.state, current_symbols))
        print((self.state, current_symbols))
        
        if action is None:
            print("no valid transition")
            return False  # No valid transition, halt
        next_state, writes, moves = action
        self.state = next_state
        
        for i in range(self.num_tapes):
            self.tapes[i][self.heads[i]] = writes[i]
            if moves[i] == 'R':
                self.heads[i] += 1
                if self.heads[i] == len(self.tapes[i]):
                    self.tapes[i].append('B')
            elif moves[i] == 'L':
                if self.heads[i] > 0:
                    self.heads[i] -= 1
        
        return True  # Valid transition executed

    def execute(self, inputs):
        for i, input_str in enumerate(inputs):
            self.tapes[i] = list(input_str) + ['B']
            self.heads[i] = 0
        
        while self.state not in self.accepting_states:
            if not self.step():
                break

    def get_tapes(self):
        return [''.join(tape).strip() for tape in self.tapes]

        
# Main
initial_state = 'q_start'
accepting_states = {'q_accept'}
num_tapes = 3  # Turing machine with 3 tapes

# Initialize turing machine
mtm = TM_Multitape(num_tapes, initial_state, accepting_states, transitions)

# Input and tapes
input_strings = ['B001000100X000XB', 'BBBBBBBBBBBBBBBBBBBBBBB', 'BBBBBBBBBBBBB']

# Execute TM-Multitape
mtm.execute(input_strings)

# Get the output from the tapes
output = mtm.get_tapes()
print(output)
print("result : " + str(output[2].count('0')))