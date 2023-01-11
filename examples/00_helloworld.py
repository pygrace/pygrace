from pygrace.project import Project

# make an instance of the Project class
grace = Project()

# add a Graph as a "child" of the Project instance
graph = grace.add_graph()
graph.title.text = 'Hello, world!'

# add a simple DataSet as a "child" of the graph instance.  A list of data is
# always the required first argument to add_dataset.
data = [(0, 0), (0.5, 0.75), (1, 1)]
dataset = graph.add_dataset(data)

# print the Project to a file (.agr format)
grace.saveall('00_helloworld.agr')
