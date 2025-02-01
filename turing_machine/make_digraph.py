from graphviz import Digraph
from transitions import transitions

dot = Digraph()

# Add nodes for all states
states = set()
for (state, _), (next_state, _, _) in transitions.items():
    states.add(state)
    states.add(next_state)

for state in states:
    shape = 'doublecircle' if state.startswith('q_accept') else 'circle'
    dot.node(state, shape=shape)

# Add a start node to indicate the initial state q0
dot.node('start', shape='point')
dot.edge('start', 'q0', label='start',)  # Arrow pointing to q0 from start node (default arrowhead)

# Add edges with labels
edges = {}

def replace_blanks(symbols):
    return ''.join(['B' if s == ' ' else s for s in symbols])

# Collect edges
for (state, symbols), (next_state, writes, moves) in transitions.items():
    label_symbols = replace_blanks(symbols)
    label_writes = replace_blanks(writes)
    label = f"{label_symbols} / {label_writes}, {''.join(moves)}"
    if (state, next_state) in edges:
        edges[(state, next_state)].append(label)
    else:
        edges[(state, next_state)] = [label]

# Add edges with labels
for (state, next_state), labels in edges.items():
    combined_label = '\n'.join(labels)
    dot.edge(state, next_state, label=combined_label)

dot.render('../static/images/tm_multitape', format='pdf', cleanup=True)

dot.view('../static/images/tm_multitape')
