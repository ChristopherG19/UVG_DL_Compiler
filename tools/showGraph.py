# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

import graphviz

# Función para mostrar AFN's
def showGraphNFA(nfa, metodo):
    g = graphviz.Digraph(comment="AFN")

    g.attr(rankdir='LR')

    for estado in nfa.states:
        if estado == nfa.initialState and estado == nfa.finalState:
            g.edge('start', str(estado))
            
        if estado == nfa.initialState:
            g.edge('start', str(estado))
            g.node('start', shape='point')
        elif estado == nfa.finalState:
            g.node(str(estado), shape='doublecircle')
        else:
            g.node(str(estado), shape='circle')

    for transicion in nfa.transitions:
        origen, simbolo, destino = transicion.inState, transicion.symbol, transicion.fnState
        g.edge(str(origen), str(destino), label=str(simbolo))
        
    g.render(f'results/AFN_{metodo}',format='png')

# Función para mostrar AFD's
def showGraphDFA(dfa, metodo):
    g = graphviz.Digraph(comment="AFD")

    g.attr(rankdir='LR')

    for estado in dfa.states:
        if estado == dfa.initialState and estado in dfa.finalStates:
            g.node(str(estado), shape='doublecircle')
            
        if estado == dfa.initialState:
            g.edge('start', str(estado))
            g.node('start', shape='point')
        elif estado in dfa.finalStates:
            g.node(str(estado), shape='doublecircle')
        else:
            g.node(str(estado), shape='circle')

    for transicion in dfa.transitions:
        origen, simbolo, destino = transicion.inState, transicion.symbol, transicion.fnState
        g.edge(str(origen), str(destino), label=str(simbolo))
        
    g.render(f'results/AFD_{metodo}', format='png')