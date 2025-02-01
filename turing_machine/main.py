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
        
        if action is None:
            print("\nNo valid transition or division by zero")
            return False
        next_state, writes, moves = action
        self.state = next_state

        print(f"Current State: {self.state}")
        print(f"Current Symbols: {current_symbols}")
        
        max_tape_length = max(len(''.join(tape).strip()) for tape in self.tapes)
        for i, tape in enumerate(self.tapes):
            tape_str = ''.join(tape).strip()
            head_pos = self.heads[i]
            
            arrow = [' '] * max_tape_length
            if head_pos < len(tape_str):
                arrow[head_pos] = '^'
            
            arrow_str = ''.join(arrow)
            
            print(f"Tape {i+1}: {tape_str}")
            print(f"        {arrow_str}")
        
        print("")
        
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