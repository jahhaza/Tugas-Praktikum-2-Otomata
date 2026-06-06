import ipywidgets as widgets
from IPython.display import display, clear_output

class PDA:
    def __init__(self, transitions, initial_state, initial_stack, final_states):
        self.transitions = transitions
        self.initial_state = initial_state
        self.initial_stack = initial_stack
        self.final_states = final_states

    def is_accepted(self, input_string):
        configs = [(self.initial_state, input_string, self.initial_stack)]
        while configs:
            curr_state, rem_input, stack = configs.pop()
            if not rem_input and curr_state in self.final_states:
                return True
            char = rem_input[0] if rem_input else None
            stack_top = stack[-1] if stack else None
            if char is not None:
                key = (curr_state, char, stack_top)
                if key in self.transitions:
                    for next_state, push_chars in self.transitions[key]:
                        new_stack = list(stack[:-1]) + (list(push_chars[::-1]) if push_chars != 'ε' else [])
                        configs.append((next_state, rem_input[1:], new_stack))
            key_eps = (curr_state, 'ε', stack_top)
            if key_eps in self.transitions:
                for next_state, push_chars in self.transitions[key_eps]:
                    new_stack = list(stack[:-1]) + (list(push_chars[::-1]) if push_chars != 'ε' else [])
                    configs.append((next_state, rem_input, new_stack))
        return False

header_html = "<div style='background-color: #1e88e5; color: white; padding: 15px; border-radius: 8px; text-align: center;'><h2>PDA Automation Dashboard</h2></div>"

trans_input = widgets.Textarea(value='q0,a,Z -> q0,AZ\nq0,b,A -> q1,ε\nq1,b,A -> q1,ε\nq1,ε,Z -> q2,Z', layout={'height': '200px', 'width': 'auto'})
init_state = widgets.Text(value='q0', description='Start State:')
final_states = widgets.Text(value='q2', description='Final States:')
init_stack = widgets.Text(value='Z', description='Start Stack:')
string_input = widgets.Text(placeholder='Ketik string di sini...', layout={'width': '70%'})
btn_run = widgets.Button(description='SIMULASI', button_style='success', icon='play', layout={'width': '28%'})
output_box = widgets.Output()
history_output = widgets.Output()

config_box = widgets.VBox([
    widgets.HTML("<b>Pengaturan Dasar:</b>"),
    widgets.HBox([init_state, final_states, init_stack]),
    widgets.HTML("<b>Definisi Transisi (state, char, pop -> next_state, push):</b>"),
    trans_input
])

simulator_box = widgets.VBox([
    widgets.HTML("<b>Masukkan String untuk Diuji:</b>"),
    widgets.HBox([string_input, btn_run]),
    output_box,
    widgets.HTML("<hr><b>Riwayat Uji:</b>"),
    history_output
])

tabs = widgets.Tab(children=[config_box, simulator_box])
tabs.set_title(0, 'Konfigurasi Mesin')
tabs.set_title(1, 'Simulator String')

def run_simulation(_):
    with output_box:
        clear_output()
        try:
            rules = {}
            for line in trans_input.value.strip().split('\n'):
                if '->' not in line: continue
                lhs, rhs = line.split('->')
                curr_s, inp, pop = [x.strip() for x in lhs.split(',')]
                next_s, push = [x.strip() for x in rhs.split(',')]
                key = (curr_s, inp, pop)
                if key not in rules: rules[key] = []
                rules[key].append((next_s, push))

            pda = PDA(rules, init_state.value.strip(), [init_stack.value.strip()], [s.strip() for s in final_states.value.split(',')])
            accepted = pda.is_accepted(string_input.value.strip())

            res_color = "#c8e6c9" if accepted else "#ffcdd2"
            text_color = "#2e7d32" if accepted else "#c62828"
            label = "ACCEPTED" if accepted else "REJECTED"

            display(widgets.HTML(f"""
                <div style='background-color: {res_color}; border: 2px solid {text_color}; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                    <h3 style='color: {text_color}; margin: 0; text-align: center;'>{label}</h3>
                </div>
            """))

            with history_output:
                display(widgets.HTML(f"• String: <code>{string_input.value}</code> → <b style='color:{text_color}'>{label}</b>"))

        except Exception as e:
            display(widgets.HTML(f"<div style='color:red;'><b>Error:</b> {str(e)}</div>"))

btn_run.on_click(run_simulation)

display(widgets.HTML(header_html))
display(tabs)

