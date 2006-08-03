import sys, os
from sizeAdjust import adjust_labels
from grace_styles import set_style
from grace import Grace
from graph import Graph
from dataset import DataSet

#--------------------------#

readin = lambda : sys.stdin.readline()[:-1] #remove newline character

#--------------------------#

grace = Grace()

sys.stdout.write("Enter the name of the file you wish to create: ")
to_create = type = readin()

#sys.stdout.write("Enter the data type (xy for now): ")
#type = readin()

print "Enter file names.  Enter a blank line when finished."
sys.stdout.write("--> ")
file = readin()

## graph = Graph(grace._colors,grace._fonts)
## grace.add_graph(graph)

# read xy data
while not file == '':
    try:
        file = open(file)
        graph = Graph(grace._colors,grace._fonts)
        grace.add_graph(graph)
        line = file.readline()
        the_data = []
        while line:
            line = line.split()
            try:
                datumlist = []
                for i in range(len(line)):
                    try: datumlist.append(float(line[i]))
                    except: datumlist.append(str(line[i]))
                if datumlist: the_data.append(datumlist)
                line = file.readline()
                
            except:
                sys.stderr.write("ERROR READING DATA FROM THIS LINE: " + str(line) + "\n")

        dataset = DataSet(the_data,grace._colors,grace._fonts)
        graph.add_dataset(dataset)
        sys.stdout.write("   Enter legend text: ")
        dataset['legend'] = readin()

        #--------Read from another file-----------#
        sys.stderr.write("--> ")
        file = readin()
        
    except IOError: 
        print "File not found."
        sys.stderr.write("--> ")
        file = readin()
    except:
        raise
    
#---------Tile and Axis Labels----------#
## print "Titles and Axis Labels"
## sys.stdout.write("Title: ")
## graph['title']['label'] = readin()
## sys.stdout.write("Subtitle: ")
## graph['subtitle']['label'] = readin()
## sys.stdout.write("X-axis: ")
## graph['xaxis']['label']['label']['label'] = readin()
## sys.stdout.write("Y-axis: ")
## graph['yaxis']['label']['label']['label'] = readin()


grace.multi(2,2)
set_style('lin',grace)

#graph = grace.get_rc(0,0)
#graph['yaxis']['label']['label']['label'] = 'This is a test.'

print "FINISHED"

if not to_create.split('.')[-1].upper() == 'AGR':
    to_create = to_create + '.agr'


for graph in grace.graphs:
   adjust_labels(graph,IncreaseOnly=False)
grace.write_agr(to_create)
command = 'xmgrace -autoscale xy ' + to_create + ' &'
os.system(command)
