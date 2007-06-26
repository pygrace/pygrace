import sys, os
sys.path.append('./PyGrace/trunk/')
from grace import Grace
from graph import Graph
from dataset import DataSet
from regression import expreg,pwrreg

grace = Grace()
graph = Graph(grace._colors,grace._fonts)
grace.add_graph(graph)

#readin = lambda : sys.stdin.readline()[:-1] #remove newline character
file="Exp_4000_128.cum";

file = open(file)
x, y = zip(*[map(float, line.strip().split()) for line in file if line])
file.close()

the_data=zip(x,y)
dataset = DataSet(the_data,grace._colors,grace._fonts)
graph.add_dataset(dataset)
    
slope,intercept,regcoeff,the_data=expreg(x,y)
dataset = DataSet(the_data,grace._colors,grace._fonts)
dataset.line.color="red"
graph.add_dataset(dataset)

slope,intercept,regcoeff,the_data=pwrreg(x,y)
dataset = DataSet(the_data,grace._colors,grace._fonts)
dataset.line.color="blue"
graph.add_dataset(dataset)

grace.write_agr('bollocks.agr')
#command = 'xmgrace -autoscale xy bollocks.agr &'
#os.system(command)
