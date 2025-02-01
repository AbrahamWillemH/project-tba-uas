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
        
        print(f"Current State: {self.state}")
        print(f"Current Symbols: {current_symbols}")
        for i, tape in enumerate(self.tapes):
            tape_str = ''.join(tape).strip()
            head_pos = self.heads[i]
            print(f"Tape {i+1}: {tape_str} (Head at {head_pos})")
        print("")

        if action is None:
            print("\nNo valid transition.")
            return False

        next_state, writes, moves = action
        self.state = next_state

        for i in range(self.num_tapes):
            self.tapes[i][self.heads[i]] = writes[i]
            if moves[i] == 'R':
                self.heads[i] += 1
                if self.heads[i] == len(self.tapes[i]):
                    self.tapes[i].append(' ')
            elif moves[i] == 'L':
                if self.heads[i] > 0:
                    self.heads[i] -= 1
                else:
                    self.tapes[i].insert(0, ' ')
                    self.heads[i] = 0
        
        return True

    def execute(self, inputs):
        for i, input_str in enumerate(inputs):
            self.tapes[i] = [' '] + list(input_str.replace('B', ' ')) + [' ']
            self.heads[i] = 1
        
        while self.state not in self.accepting_states:
            if not self.step():
                break

    def get_tapes(self):
        return [''.join(tape).strip() for tape in self.tapes]
    
    def count_zeros_on_third_tape(self):
        if len(self.tapes) < 3:
            return 0
        return self.tapes[2].count('0')

# Define the Turing machine
num_tapes = 3
initial_state = 'q0'
accepting_states = {'q_accept'}

# Create the Turing machine instance
tm = TM_Multitape(num_tapes, initial_state, accepting_states, transitions)

# Set input on the tapes
inputs = ['00010010001001', ' ', ' ']

# Run the Turing machine
tm.execute(inputs)

# Output the final tapes content
print("Final Tape 1:", tm.get_tapes()[0])
print("Final Tape 2:", tm.get_tapes()[1])
print("Final Tape 3:", tm.get_tapes()[2])

# Count zeros on the third tape
print("Number of '0's on Tape 3:", tm.count_zeros_on_third_tape())
