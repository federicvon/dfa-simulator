import streamlit as st
import graphviz
from streamlit_autorefresh import st_autorefresh

#transitions
dfa1 = {
    "states": list(range(11)),
    "alphabet": ['a', 'b'],
    "start_state": 0,
    "accept_states": [10],
    "transitions": {
        0: {'a': 1, 'b': 1},
        1: {'a': 2, 'b': 2},
        2: {'a': 3, 'b': 5},
        3: {'a': 3, 'b': 4},
        4: {'a': 7, 'b': 8},
        5: {'a': 6, 'b': 5},
        6: {'a': 7, 'b': 9},
        7: {'a': 10, 'b': 10},
        8: {'a': 9, 'b': 10},
        9: {'a': 7, 'b': 10},
        10: {'a': 10, 'b': 10},
    }
}

dfa2 = {
   "states":  list(range(17)),
    "alphabet": ['0', '1'],
    "start_state": 0,
    "accept_states": [13,15,16],
    "transitions": {
        0: {'0': 1, '1': 1},
        1: {'0': 2, '1': 2},
        2: {'0': 3, '1': 3},
        3: {'0': 4, '1': 5},
        4: {'0': 6, '1': 5},
        5: {'0': 8, '1': 10},
        6: {'0': 7, '1': 7},
        7: {'0': 17, '1': 11},
        8: {'0': 6, '1': 9},
        9: {'0': 7, '1': 10},
        10: {'0': 6, '1': 7},
        11: {'0': 14, '1': 12},
        12: {'0': 14, '1': 13},
        13: {'0': 14, '1': 13},
        14: {'0': 17, '1': 15},
        15: {'0': 16, '1': 13},
        16: {'0': 17, '1': 15},
        17: {'0': 17, '1': 18},
        18: {'0': 16, '1': 13}

    }
}
#graphviz things
def draw_step_graph(states, accept_states, transitions, path, current_index):
    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR'})
    for state in states:
        shape = 'doublecircle' if state in accept_states else 'circle'
        color = 'green' if state in accept_states else 'black'
        if current_index < len(path) and state == path[current_index]:
            dot.node(str(state), shape=shape, style='filled', fillcolor='lightblue', color=color)
        else:
            dot.node(str(state), shape=shape, color=color)

    for from_state, paths in transitions.items():
        for symbol, to_state in paths.items():
            color = 'red' if (
                current_index > 0 and path[current_index - 1] == from_state and path[current_index] == to_state
            ) else 'black'
            penwidth = '2' if color == 'red' else '1'
            dot.edge(str(from_state), str(to_state), label=symbol, color=color, penwidth=penwidth)

    return dot

def simulate_dfa(start_state, alphabet, transitions, accept_states, input_str):
    current_state = start_state
    path = [current_state]
    for char in input_str:
        if char not in alphabet:
            return False, path, f"Invalid character: {char}"
        if char in transitions[current_state]:
            current_state = transitions[current_state][char]
            path.append(current_state)
        else:
            return False, path, "No transition found"
    return current_state in accept_states, path, None

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "DFA 1 Simulator", "DFA 2 Simulator"])

if page == "Home":
    st.title("DFA Simulator")
    st.write("### Instructions for using the application:")
    st.markdown("""
### **1. DFA 1:**  
**Regular Expression:**  
`(a + b + aa + bb + aba)(a + b + bb + aa)*(a + b + aa + bb)(a + b)*(ab + ba + bab + aba)(ab + bb + abb + bab + aa)(a + b)*`  

**Instructions:**  
Following the alphabet `{a, b}`, enter a string and click **Start Simulation** to test your string.  
The simulator will automatically trace your string to determine if it's valid or invalid.

**Language Description:**  
- Must start with any of the following: `a`, `b`, `aa`, `bb`, `aba`  
- Must have at least one occurrence of the following: `a`, `b`, `aa`, `bb`  
- May be followed by any number of `a`s and `b`s  
- Must be followed by any of the following: `ab`, `ba`, `bab`, `aba`  
- Must be followed by any of the following: `ab`, `bb`, `abb`, `bab`, `aa`  
- May be followed by any sequence of `a`s and `b`s  

---

### **2. DFA 2:**  
**Regular Expression:**  
`(1+0)(1+0)*(11+00+01+10)*(11+00+01+10)(1010+001+111+000)(1+0)*(101+011+111+010)`  

**Instructions:**  
Following the alphabet `{0, 1}`, enter a string and click **Start Simulation** to test your string.  
The simulator will automatically trace your string to determine if it's valid or invalid.

**Language Description:**  
- Must start with `1` or `0`  
- After the first letter, any number of `1`s and `0`s can be accepted  
- Must have at least one pair of binary patterns: `00`, `01`, `10`, `11`  
- Must include one of the following sequences: `1010`, `001`, `111`, `000`  
- Can be followed with any number of `1`s and `0`s  
- Must end with one of the following sequences: `101`, `011`, `111`, `010`  
""")

    st.markdown("--------")

    st.markdown("""
**Made by:**  
Secret 
** **
""")


                
    st.stop()

# Select DFA
dfa = dfa1 if page == "DFA 1 Simulator" else dfa2
dfa_name = "DFA 1" if page == "DFA 1 Simulator" else "DFA 2"

states = dfa["states"]
alphabet = dfa["alphabet"]
start_state = dfa["start_state"]
accept_states = dfa["accept_states"]
transitions = dfa["transitions"]

input_key = f"input_str_{dfa_name}"
path_key = f"path_{dfa_name}"
step_key = f"current_step_{dfa_name}"
finished_key = f"finished_{dfa_name}"

if input_key not in st.session_state:
    st.session_state[input_key] = ""
if path_key not in st.session_state:
    st.session_state[path_key] = []
if step_key not in st.session_state:
    st.session_state[step_key] = 0
if finished_key not in st.session_state:
    st.session_state[finished_key] = False

st.title(f"{dfa_name} Simulator")

if page == "DFA 1 Simulator":
    st.markdown("Regular Expression: (a + b + aa + bb + aba)(a + b + bb + aa)*(a + b + aa + bb)(a + b)*(ab + ba + bab + aba)(ab + bb + abb + bab + aa)(a + b)*")
    st.markdown("""**Sample Strings:**

- `aababababaa` 
- `babbababb`
- `abaabababbbab`  
- `aaababbabbbaa`  
- `baababababb`   
""")

if page == "DFA 2 Simulator":
    st.markdown("Regular Expression: ((1+0)(1+0)*(11+00+01+10)*(11+00+01+10)(1010+001+111+000)(1+0)*(101+011+111+010)")
    st.markdown("""**Sample Strings:**

- `110111010000111`
- `111000111010`
- `101000101011`
- `1001111010`
- `011000111011`
""")


user_input = st.text_input(f"Enter a string using {alphabet}:", value=st.session_state[input_key])

if st.button("Start Simulation"):
    accepted, path, error = simulate_dfa(start_state, alphabet, transitions, accept_states, user_input)
    if error:
        st.error(error)
    else:
        st.session_state[input_key] = user_input
        st.session_state[path_key] = path
        st.session_state[step_key] = 0
        st.session_state[finished_key] = False
        
path = st.session_state.get(path_key, [start_state])
current_index = st.session_state.get(step_key, 0)


st.subheader("DFA Visualization")
st.graphviz_chart(draw_step_graph(states, accept_states, transitions, path, current_index))

# if simulation is running or completed, show step and result
if len(path) > 1:
    st.write(f"Step {current_index}: State {path[current_index]}")

    if not st.session_state[finished_key]:
        st_autorefresh(interval=1000, key=f"autorefresh_{dfa_name}")
        if current_index < len(path) - 1:
            st.session_state[step_key] += 1
        else:
            st.session_state[finished_key] = True

    # show final result when done
    if st.session_state[finished_key]:
        if path[-1] in accept_states:
            st.success("✅ String Valid! 😊 ")
        else:
            st.warning("❌ String Invalid 🥺 ")

if page == "DFA 1 Simulator":
    st.markdown("### Context-Free Grammar (CFG) for DFA 1:")
    st.code("""S → A X B C D E F
A → a | b | aa | bb | aba
X → aX | bX | bbX | aaX | ε
B → a | b | aa | bb
C → aC | bC | ε
D → ab | ba | bab | aba
E → ab | bb | abb | bab | aa
F → aF | bF | ε""", language="text")

    st.markdown("### PDA Visualization:")
    st.image("PDAAB.jpg", caption="Pushdown Automaton for the Language", use_container_width=True)

if page == "DFA 2 Simulator":
   
    st.markdown("### Context-Free Grammar (CFG) for DFA 2:")
    st.code("""S → AXYBCXD
A → 1 | 0 
X → 1X | 0X | ε
Y → 11Y | 00Y | 01Y | 10Y | ε
B → 11 | 00 | 01 | 10 | ε
C → 1010 | 001 | 111 | 000 | ε
D → 101 | 011 | 111 | 010""", language="text")  #

    st.markdown("### PDA Visualization for DFA 2:")
    st.image("PDA01.jpg", caption="Pushdown Automaton for DFA 2", use_container_width=True)  

