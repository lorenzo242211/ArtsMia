from model.model import Model

mdl = Model()
mdl.buildGraph()
print(f"grafo dio {mdl.getNumNodes()} {mdl.getNumEdges()}")
prime15 = list(mdl.grafo.edges(data=True))[:20]
for nodo in prime15:
    print(f"{nodo[0].object_id} -> {nodo[1].object_id} | peso = {nodo[2]['weight']}")

