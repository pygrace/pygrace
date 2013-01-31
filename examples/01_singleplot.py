from pygrace.plot import Plot
from pygrace.colors import ColorBrewerScheme

# ---------------------------------- this is the part where YOU do the analysis
# data1 and data2 are both lists of (x, y) points.
import example_tools
data1, data2 = example_tools.singleplot()

grace = Plot(colors=ColorBrewerScheme('Paired'))

graph = grace.add_graph()
graph.xaxis.label.text = 'Fake X'
graph.yaxis.label.text = 'Fake Y'

dataset1 = graph.add_dataset(data1, legend='Set 1')
dataset1.symbol.fill_color = 'Paired-0'

dataset2 = graph.add_dataset(data2, legend='Set 2')
dataset2.symbol.fill_color = 'Paired-1'

graph.set_world_to_limits()
graph.logxy()

grace.write_file('01_singleplot.agr')

