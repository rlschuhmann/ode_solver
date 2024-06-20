import networkx as nx
import streamlit as st

# create placeholder flowchart - i.e. a directed graph
G = nx.DiGraph()
start = r"Let's start with this: does your differential equation contain derivatives with respect to more than variable? For example, you may have both $\frac{\partial}{\partial t}$ and $\frac{\partial}{\partial x}$ in the equation?"
G.add_node(0, label=start)
is_ode = "Then it is an ODE! Let's standardise things a little: from now on, the variable with respect to which we derive is always called $x$. Is there more than one function of $x$ kicking around in your equation?"
is_pde = "This is not an ODE, but rather a partial differential equation (PDE). These are much more advanced and require completely different techniques."
G.add_node(1, label=is_ode)
G.add_node(2, label=is_pde)

G.add_edge(0, 1, label='no')
G.add_edge(0, 2, label='yes')

# add return edges
for node in G.nodes:
    if node != 0:
        G.add_edge(node, 0, label='return to start')

# helper function that extracts outgoing edge labels and target nodes from node number
def get_desc_node_data(node):
    out_edges = G.out_edges(node, data=True)
    return {edge_data['label']: tail for head, tail, edge_data in out_edges}

# streamlit stuff begins here

# keep track of where in the graph we are
if "current_node" not in st.session_state:
    st.session_state.current_node = 0

# this renders the label of the current node, and a button for every outgoing edge
@st.experimental_fragment
def draw_buttons():
    current_node = st.session_state.current_node
    st.markdown(G.nodes[current_node]['label'])
    node_data = get_desc_node_data(current_node)
    if node_data: # may be empty if terminal node
        cols = st.columns(len(node_data))
        for (reply, next_node), col in zip(sorted(node_data.items(), reverse=True), cols):
            # define callback that traverses the clicked edge
            def on_click():
                st.session_state.current_node = next_node
            # render button
            col.button(label=reply, on_click=on_click)

# streamlit app rendering begins here
st.title("So you've got this ODE ...")
draw_buttons()