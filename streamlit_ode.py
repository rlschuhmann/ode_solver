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

G.add_edge(0, 1, label='no, just one kind of derivative')
G.add_edge(0, 2, label='yes, more than one')

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
G.add_edge(1, 3, label='just one function')
G.add_edge(1, 4, label='more than one')

is_firstorder = r'''
So we have a single first-order ODE. Does the right-hand side $F$ depend on $x$ or $y$ at all?
'''
is_higher_than_first_order = r"Is $n=2$?"
G.add_node(5, label=is_firstorder)
G.add_node(6, label=is_higher_than_first_order)
G.add_edge(3, 5, label='yes, first order')
G.add_edge(3, 6, label='no, higher order')

can_be_integrated_directly = r'''
You're in luck! This ODE is as simple as can be. You can just throw an integral onto the RHS and write
$$
y(x) = y_0 + \int_{x_0}^{x} d\tilde x\,F(\tilde x),
$$
where $y(x_0)=y_0$ is your given initial condition.
'''
is_autonomous = r'''
So your equation looks like 
$$
y'(x) = F(y).
$$
This is known as an _autonomous_ ODE. We can solve it like a separable one: shuffle all $y$-dependent stuff onto the LHS, all, $x$-dependent stuff onto the RHS, and integrate:
$$
\int \frac{dy}{g(y)} = \int dx + C,
$$
or if you'd prefer to avoid futzing around with the integration constant $C$ in favour of the initial value $y(x_0) = y_0$, then you may write it as
$$
\int_{y_0}^{y(x)} \frac{d\tilde y}{g(\tilde y)} = \int_{x_0}^x d\tilde x = x - x_0.
$$
Now all that is left to do is: crack the LHS integral, and manipulate until you manage to isolate $y(x)$.

You will notice that $y(x)$ depends only on the distance to the starting point $x-x_0$. This is a general and very useful feature of autonomous ODEs.
'''
is_nonautonomous = r'''
So your equation looks like
$$
y'(x) = F(x, y).
$$
Does the RHS perhaps factorise like this: $F(x, y) = f(x)g(y)$?
'''
G.add_node(7, label=can_be_integrated_directly)
G.add_node(8, label=is_autonomous)
G.add_node(9, label=is_nonautonomous)
G.add_edge(5, 7, label='$F$ is a function of $x$ only')
G.add_edge(5, 8, label='$F$ is a function $y$ only')
G.add_edge(5, 9, label='$F$ contains both variables')

is_separable = r'''
Nice! This means that your ODE is _separable_. What this means is that you can accumulate everything $y$-dependent on the LHS, and everything $x$-dependent on the RHS, and integrate:
$$
\frac{dy}{dx} = f(x)g(y) \Rightarrow \int \frac{dy}{g(y)} = \int dx\,f(x) + C,
$$
where we can mash both integration constants into one. Now you need to crack both integrals, and isolate $y(x)$ on the LHS, and you are done.
If you have an initial value $y(x_0) = y_0$, then you can write this cleaner by incorporating it - obviously that will remove the integration constant $C$:
$$
\int_{y_0}^{y(x)} d\tilde y\frac{1}{g(\tilde y)} = \int_{x_0}^xd\tilde x f(\tilde x)
$$
'''
G.add_node(10, label=is_separable)
G.add_edge(9, 10, label='yes, it factorises')
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

if "node_history" not in st.session_state:
    st.session_state.node_history = [st.session_state.current_node]

# this renders the label of the current node, and a button for every outgoing edge
@st.experimental_fragment
def draw_buttons():
    current_node = st.session_state.current_node
    #st.text(f'current node number: {current_node}')
    st.markdown(G.nodes[current_node]['label'])
    node_data = get_desc_node_data(current_node)
    #st.text(f'outgoing data: {node_data}')
    if node_data: # may be empty if terminal node
        # render one extra button if we are not at the start
        if len(st.session_state.node_history) > 1:
            ncols = len(node_data) + 1
            cols = st.columns(ncols)
            cols_for_desc_nodes = cols[:-1]            
        else:
            ncols = len(node_data)
            cols = st.columns(ncols)
            cols_for_desc_nodes = cols
        for (reply, next_node), col in zip(node_data.items(), cols_for_desc_nodes):
            #st.text(reply + ' : ' + str(next_node))
            # define callback that traverses the clicked edge
            def traverse_graph(next_node):
                st.session_state.current_node = next_node
                st.session_state.node_history.append(next_node)

            # render buttons
            col.button(label=reply, on_click=traverse_graph, args=[next_node])
        
        # render one extra button for "go back"
        def go_back():
            st.session_state.node_history = st.session_state.node_history[:-1]
            st.session_state.current_node = st.session_state.node_history[-1]
        if len(st.session_state.node_history) > 1:
            cols[-1].button(label="go back", on_click=go_back)

# streamlit app rendering begins here
st.header("So you've got this ODE ...", divider='rainbow')
draw_buttons()
st.page_link(label="Comments? Drop me an email!", page="https://cosmorobb.science")