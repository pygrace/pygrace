from PyGrace.grace import Grace

# make an instance of the Grace class
grace = Grace()

# add a Graph as a "child" of the grace instance
graph = grace.add_graph()
graph.title.text = 'Hello, world!'

# add a simple DataSet as a "child" of the graph instance.  A list of data is
# always the required first argument to add_dataset.
data = [(0, 0), (0.5, 0.75), (1, 1)]
dataset = graph.add_dataset(data)

# print the grace to a file (.agr format)
grace.write_file('00_helloworld.agr')
