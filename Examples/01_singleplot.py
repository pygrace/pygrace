import sys
import math

# add the root directory of the PyGrace package to the PYTHONPATH
from example_tools import PYGRACE_PATH
sys.path.append(PYGRACE_PATH)

from PyGrace.grace import Grace
from PyGrace.colors import ColorBrewerScheme
from example_tools import output_name

dn = 10
x =  [10**(i/float(dn)) for i in range(-3*dn, 3*dn + 1)]
y1 = [10**math.cos(math.log10(i)**2) for i in x]
y2 = [10**math.sin(math.log10(i)**2) for i in x]

grace = Grace(colors=ColorBrewerScheme('Paired'))

graph = grace.add_graph()
graph.xaxis.label.text = 'Fake X'
graph.yaxis.label.text = 'Fake Y'

dataset1 = graph.add_dataset(zip(x, y1), legend='Set 1')
dataset1.symbol.fill_color = 'Paired-0'

dataset2 = graph.add_dataset(zip(x, y2), legend='Set 2')
dataset2.symbol.fill_color = 'Paired-1'

graph.set_world_to_limits()
graph.logxy()

# print the grace (.agr format) to a file
grace.write_file(output_name(__file__))

outStream = open(output_name(__file__), 'w')
print >> outStream, grace
outStream.close()

