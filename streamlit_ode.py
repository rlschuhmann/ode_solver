import networkx as nx
import streamlit as st

# create placeholder flowchart - i.e. a directed graph
G = nx.DiGraph()
start = r"Let's start with this: does your differential equation contain derivatives with respect to more than variable? For example, you may have both $\frac{\partial}{\partial t}$ and $\frac{\partial}{\partial x}$ in the equation?"
G.add_node(0, label=start)
is_ode = "Then it is an ODE! Let's standardise things a little: from now on, the variable with respect to which we derive is always called $x$, and $x$-derivatives will be denoted with a prime $(\ldots)'$. Is there more than one unknown function of $x$ kicking around in your equation?"
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
G.add_edge(1, 3, label='just one unknown function')
G.add_edge(1, 4, label='more than one unknown function')

is_firstorder = r'''
So we have a single first-order ODE. Does the right-hand side $F$ depend on $x$ or $y$ at all?
'''
is_higher_than_first_order = r"Is $n=2$?"
G.add_node(5, label=is_firstorder)
G.add_node(6, label=is_higher_than_first_order)
G.add_edge(3, 5, label="yes, $y'$ is the highest derivative to appear")
G.add_edge(3, 6, label='no, we have higher derivatives of $y$ than the first')

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
\int \frac{dy}{F(y)} = \int dx = x + C,
$$
or if you'd prefer to avoid futzing around with the integration constant $C$ in favour of the initial value $y(x_0) = y_0$, then you may write it as
$$
\int_{y_0}^{y(x)} \frac{d\tilde y}{F(\tilde y)} = \int_{x_0}^x d\tilde x = x - x_0.
$$
Now all that is left to do is: crack the LHS integral, and manipulate until you manage to isolate $y(x)$.

You will notice that $y(x)$ depends only on the distance to the starting point $x-x_0$. This strictly constrains the possible shape of $y(x)$, so we found a general and very useful feature of autonomous ODEs: shifting one solution in $x$-direction will again yield a solution.
'''
is_nonautonomous = r'''
So your equation looks like
$$
y'(x) = F(x, y).
$$
Does the RHS perhaps factorise like this: $F(x, y) = f(x)g(y)$? It might not be immediately obvious, so keep trying to bring it into this form.
'''
G.add_node(7, label=can_be_integrated_directly)
G.add_node(8, label=is_autonomous)
G.add_node(9, label=is_nonautonomous)
G.add_edge(5, 7, label='$F$ is a function of $x$ only')
G.add_edge(5, 8, label='$F$ is a function of $y$ only')
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
is_nonseparable = r'''
Next try: does $y$ appear only linearly, meaning in the first power and not inside some other function? In other words, can you find functions $p(x)$ and $q(x)$ _of $x$ only_ so that you can write the ODE as
$$
y' + p(x) y = q(x)?
$$
'''
G.add_node(10, label=is_separable)
G.add_node(11, label=is_nonseparable)
G.add_edge(9, 10, label='yes, it factorises')
G.add_edge(9, 11, label="I tried long enough, it won't")

is_linear_firstorder = r'''
This means that we have a _linear_ first-order ODE $y' + p(x) y = q(x)$. There is a general solution formula that applies to all of them, known by the name _integrating factor_. In its full glory it is somewhat intimidating:
$$
y = \frac{\int \mu(x) q(x) dx + C}{\mu(x)}
$$
with
$$
\mu = \exp\int p(x) dx. 
$$
If you read off $p(x)$ and $q(x)$ from comparing your ODE to the general form $y' + p(x)y = q(x)$, and plug those two functions into the above formula, you get your general solution $y(x)$ upon cracking all of the integrals.

If that formula above looks scary you, no worries! It's totally possible to solve every linear first-order ODE without ever breaking it out. There is an alternative more benign method which will get you to the solution step by step, and it also memorises easier. Ultimately, it's a matter of personal preference.
'''
G.add_node(12, label=is_linear_firstorder)
G.add_edge(11, 12, label='yes, that works!')

has_inhomogeneity_firstorder = r'''
We have a first-order ODE with an _inhomogeneity_, meaning a term that depends only on $x$. One example is the most general linear first-order form $y' + p(x)y = q(x)$. Here, the right-hand side term $q(x)$ is the inhomogeneity. 

The method to solve these is a two-step process. First, we solve a related auxiliary ODE, which is _simpler_. The solution will allow us to smartly guess an ansatz for the full ODE, leaving us with another _simpler_ ODE. 

Firstly: rewrite the ODE by dropping the inhomogeneity. This simplifies the equation - in the above example we have $y_h' + p(x) y_h = 0$ left. Since it's a different equation than the one we actually want to solve, we swapped $y(x)$ for $y_h(x)$ - the latter is the solution to our _auxiliary_ ODE. Solve this by whatever means - the above example can be cracked by separation of variables (you can review that method via the button below). Or return to start, if you began with something nonlinear. 

Either way, you should get an expression for the function $y_h(x)$ with one constant of integration, say, $C$. This $y_h(x)$ is sometimes known as the _particular_ or _complementary_ solution.

Secondly, a sleight of hand: we promote $C$ to a function of $x$. Our ansatz for $y$ is just the expression of $y_h$, except that we replace $C$ by $C(x)$. Ultimately that does only takes all our ignorance about the function $y(x)$ and mashes it into $C(x)$. When we plug that ansatz into the _full_ equation (including the inhomogeneity again!), we will receive a first-order ODE for $C(x)$. But, as if by magic, many terms will drop out! In the end the ODE for $C(x)$ will be easier than the original one for $y(x)$ - you can return to start to crack it.

For reasons that are probably obvious, this trick is known as _variation of constants_. It can also be applied to higher-order ODEs - except that there you have as many unknown functions as you have constants of integration in your particular solution, so it's going to be more complicated.
'''
has_inhomogeneity_higherorder = r'''
TBD
'''
G.add_node(13, label=has_inhomogeneity_firstorder)
G.add_node(14, label=has_inhomogeneity_higherorder)
G.add_edge(12, 13, label='please take me to the alternative method')
G.add_edge(13, 10, label='please take me to separation of variables')
G.add_edge(13, 14, label='please tell me more how to apply this to higher-order ODEs')
G.add_edge(14, 13, label='please let me review variation of constants for first-order ODEs')
G.add_edge(13, 14)
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

        container = st.container()
        for (reply, next_node) in node_data.items():
            #st.text(reply + ' : ' + str(next_node))
            # define callback that traverses the clicked edge
            def traverse_graph(next_node):
                st.session_state.current_node = next_node
                st.session_state.node_history.append(next_node)

            # render buttons
            container.button(label=reply, 
                             on_click=traverse_graph, 
                             args=[next_node],
                             use_container_width=True)

        
        # render one extra button for "go back"
        def go_back():
            st.session_state.node_history = st.session_state.node_history[:-1]
            st.session_state.current_node = st.session_state.node_history[-1]
        if len(st.session_state.node_history) > 1:
            container.button(label="go back", 
                             on_click=go_back,
                             use_container_width=True)

# streamlit app rendering begins here
st.header("So you've got this ODE ...", divider='rainbow')
draw_buttons()
st.page_link(label="Comments? Drop me an email!", page="https://cosmorobb.science")