import networkx as nx
import community as c
import matplotlib.pyplot as plt
import sys
import pylab
import copy

pylab.show()

#returns subgraphs after removing edges with maximum betweeness from the original graph
def removeEdges(G): 
	remove = [] #stores edges having maximum betweenness which needs to be removed from graph
	b = nx.edge_betweenness_centrality(G)
	max_betweenness = b[max(b,key=b.get)]
	for k,v in b.iteritems():
	    if v==max_betweenness:
	        remove.append(k)
	
	G.remove_edges_from(remove) # remove edges from G with max betwenness
	graphs = list(nx.connected_component_subgraphs(G))

	d={}
	counter = 0
	for graph in graphs:
		counter+=1
		for node in graph:
			d[node]=counter

	if G.number_of_edges() == 0:
		return [list(nx.connected_component_subgraphs(G)),0,G]

	modularity = c.modularity(d,G)
	return [list(nx.connected_component_subgraphs(G)),modularity,G]
		

if __name__=="__main__":
	if len(sys.argv)!=3:
		print "Usage: detect_communities <inputfile> <outputfile>"
		print "Inputfile : Contains represenation of the graph"
		print "Outputfile : This file store community visualization"
		exit(-1)
	fname = sys.argv[1]
	with open(fname) as f:
		content = f.readlines()

	result_communities=[]
	G = nx.read_edgelist("input1")
	copyGraph = copy.deepcopy(G)
	d={}
	for node in G:
		d[node]=0	
	
	initial_modularity = c.modularity(d,G)
	result_communities.append([d,initial_modularity,G])

	while G.number_of_edges()>0:
		subgraphs = removeEdges(G)
		result_communities.append(subgraphs)
		G=subgraphs[-1]
	
	for step in result_communities:
		# print ("modularity",step[1])
		if step[1]>initial_modularity:
			ng=step[0]
			result=[]
			modularity=step[1]
			
			for graph in step[0]:
				result.append(sorted([int(vertex) for vertex in graph]))
				
	
	for community in result:
		print community

	d={};counter=0
	
	for graph in ng:
		for node in graph:
			d[node] = counter 
		counter+=1

	

	pos=nx.spring_layout(copyGraph)
	colors = ["violet","black","orange","cyan","red","blue","green","yellow","indigo","pink"]
	for i in range(len(ng)):
		graph=ng[i]
		nlist = [node for node in graph]
		nx.draw_networkx_nodes(copyGraph,pos,nodelist=nlist,node_color=colors[i%10],node_size=500,alpha=0.8)

	nx.draw_networkx_edges(copyGraph,pos)
	nx.draw_networkx_labels(copyGraph,pos,font_size=10)
	plt.axis('off')
	plt.savefig(sys.argv[2]) # save as png
	
