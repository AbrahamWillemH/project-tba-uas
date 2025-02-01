from flask import Flask, request, render_template
from turing_machine.transitions import transitions
from turing_machine.main import TM_Multitape

app = Flask(__name__)

# Initialize Turing machine (instance of TM_Multitape) and other necessary setup
initial_state = 'q0'
accepting_states = {'q_accept'}
num_tapes = 3  # Turing machine with 3 tapes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_tape = request.form['input_tape']

        input_strings = [input_tape, '', '']

        # Execute the Turing machine
        mtm = TM_Multitape(num_tapes, initial_state, accepting_states, transitions)
        mtm.execute(input_strings)

        output = mtm.get_tapes()

        final_tape1 = output[0]
        final_tape2 = output[1]
        final_tape3 = output[2]

        # Prepare output tapes for display
        chunk_size = 30
        tape1_print = '\n'.join(final_tape1[i:i+chunk_size] for i in range(0, len(final_tape1), chunk_size))
        tape2_print = '\n'.join(final_tape2[i:i+chunk_size] for i in range(0, len(final_tape2), chunk_size))
        tape3_print = '\n'.join(final_tape3[i:i+chunk_size] for i in range(0, len(final_tape3), chunk_size))

        # Get head positions
        head_positions = mtm.heads

        result = {
            'initial_tape': input_strings,
            'final_tape1': tape1_print,
            'final_tape2': tape2_print,
            'final_tape3': tape3_print,
            'head_positions': head_positions,
            'result_message': output[2].count('0') if '1' not in output else "0" if output[2] == '' else ''
        }

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
