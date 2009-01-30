import sys

# add the root directory of the PyGrace package to the PYTHONPATH
from example_tools import PYGRACE_PATH
sys.path.append(PYGRACE_PATH)

from PyGrace.grace import Grace
from example_tools import output_name

# make an instance of the Grace class
grace = Grace()

# add a Graph as a "child" of the grace instance
graph = grace.add_graph()
graph.title.text = 'Hello, world!'

# add a simple DataSet as a "child" of the graph instance.  A list of data is
# always the required first argument to add_dataset.
data = [(0, 0), (0.5, 0.75), (1, 1)]
dataset = graph.add_dataset(data)

# print the grace (.agr format) to a file
grace.write_file(output_name(__file__))

# Two other methods of output are common: (i) 'print grace' writes the grace
# file to standard out, and (ii) grace.write_agr(filename)

