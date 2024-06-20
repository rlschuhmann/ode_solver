import networkx as nx
import streamlit as st

# create placeholder flowchart - i.e. a directed graph
G = nx.DiGraph()
start = r"Let's start with this: does your differential equation contain derivatives with respect to more than variable? For example, you may have both $\frac{\partial}{\partial t}$ and $\frac{\partial}{\partial x}$ in the equation?"
G.add_node(0, label=start)
is_ode = "Then it is an ODE! Let's standardise things a little: from now on, the variable with respect to which we derive is always called $x$. Is there more than one unknown function of $x$ kicking around in your equation?"
is_pde = "This is not an ODE, but rather a partial differential equation (PDE). These are much more advanced and require completely different techniques."
G.add_node(1, label=is_ode)
G.add_node(2, label=is_pde)

G.add_edge(0, 1, label='no')
G.add_edge(0, 2, label='yes')

is_single_ode = r'''
Let's standardise further: we have a single unknown function, let's call it $y(x)$. Rearrange your equation such that the highest derivative is isolated on the left hand side. Your equation now looks like 
$$
y^{(n)}(x) = \frac{d^n y(x)}{dx^n} = F\left(x, y, y', y'', \ldots, y^{(n-1)}\right)
$$
for some possibly complicated function $F(\ldots)$. 
The order of the highest derivative, $n$, is now the _order of your ODE_. 

Is $n=1$?
'''
is_coupled_ode_system = "Looks like you have a system of coupled ODEs. "

G.add_node(3, label=is_single_ode)
G.add_node(4, label=is_coupled_ode_system)
G.add_edge(1, 3, label='no')
G.add_edge(1, 4, label='yes')

is_firstorder = r'''
So we have a single first-order ODE. Does the right-hand side $F$ contain $y$ at all?
'''
is_higher_than_first_order = r"Is $n=2$?"
G.add_node(5, label=is_firstorder)
G.add_node(6, label=is_higher_than_first_order)
G.add_edge(3, 5, label='yes')
#G.add_edge(3, 6, label='no')

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
    #st.text(f'current node number: {current_node}')
    st.markdown(G.nodes[current_node]['label'])
    node_data = get_desc_node_data(current_node)
    #st.text(f'outgoing data: {node_data}')
    if node_data: # may be empty if terminal node
        cols = st.columns(len(node_data))
        for (reply, next_node), col in zip(node_data.items(), cols):
            #st.text(reply + ' : ' + str(next_node))
            # define callback that traverses the clicked edge
            def on_click(next_node):
                st.session_state.current_node = next_node
            # render button
            col.button(label=reply, on_click=on_click, args=[next_node])

# streamlit app rendering begins here
st.title("So you've got this ODE ...")
draw_buttons()