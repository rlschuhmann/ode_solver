import networkx as nx
import streamlit as st

# create placeholder flowchart - i.e. a directed graph
G = nx.DiGraph()
start = 'Does your differential equation contain derivatives with respect to more than variable?'
G.add_node(0, label=start)
is_ode = 'Then it is an ODE!'
is_pde = 'This is not an ODE, but rather a partial differential equation (PDE). These are much more advanced and require completely different techniques.'
G.add_node(1, label=is_ode)
G.add_node(2, label=is_pde)

G.add_edge(0, 1, label='yes')
G.add_edge(0, 2, label='no')
G.add_edge(2, 0, label='return to start')


st.title("So you've got this ODE ...")
