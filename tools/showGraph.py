# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# Diseño de lenguajes
# Christopher García 20541

import graphviz

def showGraph(nfa):
    g = graphviz.Digraph(comment="AFN")

    g.attr(rankdir='LR')

    for estado in nfa.states:
        if estado == nfa.initialState:
            g.edge('start', str(estado))
            g.node('start', shape='point')
            g.node(str(estado), shape='circle', style='bold')
        elif estado == nfa.finalState:
            g.node(str(estado), shape='doublecircle')
        else:
            g.node(str(estado), shape='circle')

    for transicion in nfa.transitions:
        origen, simbolo, destino = transicion.inState, transicion.symbol, transicion.fnState
        g.edge(str(origen), str(destino), label=str(simbolo))
        
    g.render("AFN", view=True)