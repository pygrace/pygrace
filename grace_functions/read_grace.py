import sys

import re #regular expressions

from grace import Grace
from graph import Graph
from dataset import DataSet
from colors import DEFAULT_COLORS, Color
from fonts import DEFAULT_FONTS, Font
from drawing_objects import Box,Text, Line
from view import View,World

from xmg_exceptions import MalformedPage


grace = Grace()
graph = Graph(grace._colors, grace._fonts)
grace.reset_colors()
grace.reset_fonts()

#--------------------------------------#

fpat = re.compile(r'-?[0-9]+.?[0-9]*') #pattern for any float or int

#--------------------------------------#

#--------------------------------------#

qpat = re.compile(r'".*"')             #pattern for text in quotes

#--------------------------------------#


#*********************  make_object function  *******************************#

def make_object(name=sys.argv[1]):
    
    file = open(name,'r') #open file - read raw strings
    
    line = file.readline()
    

    while line:
        
        #-------------------------# if there is a string in quotes, store it before splitting line
        qmatch = qpat.search(line)
        quoted = ''
        if qmatch:  
            quoted = qmatch.group()[1:-1]
        #-------------------------#  pattern for drawing objects

        draw_object_match = re.compile(r'@    ((line)|(string)|(box))').search(line)

        #-------------------------#

        line = line.replace(',',' ') #strip commas from string
        line = line.replace('(',' ')
        line = line.replace(')',' ') #remove parens (makes color parsing easier)
        line = line.split()          #split around whitespace

        #----pattern for graph identifier----# e.g. @g0

        graph_pattern = re.compile('@g[0-9]+')
        graph_match = graph_pattern.match(line[0])

        #----pattern for dataset identifier----# e.g. s0
        try:
            dataset_pattern = re.compile('s[0-9]+')
            set_match = dataset_pattern.match(line[1])
        except:
            set_match = None
        #--------------------------------------#

        if line[0] == '@version':
            grace['version'] = line[1]

        elif line[0] == '@page' and line[1] == 'size':
            grace['width'] = line[2]
            grace['height'] = line[-1]

        elif line[0] == '@background':
            if line[1] == 'color':
                grace['background_color'] = line[2]

        elif line[0] == '@page':
            if line[1] == 'background' and line[2] == 'fill':
                grace['background_fill'] = line[3]
        
        elif line[0] == '@map': #map fonts and colors
            try:
                if line[1] == 'font':
                    theFont = line[-2]
                    theFont = theFont.replace('"','')
                    nickname = line[-1]
                    nickname = nickname.replace('"','')
                    if grace._fonts.has_key(theFont):
                        pass
                    else:
                        grace.define_font(nickname, theFont)
                elif line[1] == 'color':
                    theColor = line[-1]
                    theColor = theColor.replace('"','')
                    if grace._colors.has_key(theColor):
                        pass
                    else:
                        grace.define_color(theColor, (int(line[-4]),int(line[-3]),int(line[-2])))
                else:
                    MalformedPage(line)
            except:
                MalformedPage(line)
                
        elif line[0] == '@timestamp':
            if line[1] == 'on' or line[1] == 'off':
                grace['timestamp']['onoff'] = line[1]
            elif fpat.match(line[1]) and fpat.match(line[2]):
                grace['timestamp']['x'] = line[1]
                grace['timestamp']['y'] = line[2]
            elif line[1] == 'color':
                grace['timestamp']['color'] = line[2]
            elif line[1] == 'rot':
                grace['timestamp']['rot'] = line[2]
            elif line[1] == 'font':
                grace['timestamp']['font'] = line[2]
            elif line[1] == 'char':
                grace['timestamp']['char_size'] = line[3]
            else:
                pass

        elif graph_match and graph_match.start() == 0:
            # -- determine which graph to read data into -- #
            gnum = line[0]
            id = int(gnum[2:])
            graph = grace.get_graph(id)
            if not graph:
                graph = Graph(grace._colors, grace._fonts)
                id = grace.add_graph(graph)
            if line[1] in ['on','off']:
                graph['onoff'] = line[1]
            elif line[1] == 'fixedpoint':
                pass #FOR NOW
            elif line[1] == 'bar':
                graph['bar_hgap'] = line[3]
            else:
                graph[line[1]] = line[2]

        elif line[0] == '@with':
            if re.compile('g[0-9]+').match(line[1]):
                try:
                    # -- determine which graph to read data into -- #
                    gnum = line[1]
                    id = int(gnum[1:])
                    graph = grace.get_graph(id)
                    if not graph:
                        graph = Graph(grace._colors, grace._fonts)
                        id = grace.add_graph(graph)
                except:
                        MalformedPage(line)
            elif line[1] == 'box': # -- determine which drawing object to read data into -- #
                box = Box(grace._colors,grace._fonts)
                grace.add_drawing_object(box)
            elif line[1] == 'string':
                text = Text(grace._colors,grace._fonts)
                grace.add_drawing_object(text)
            elif line[1] == 'line':
                line_obj = Line(grace._colors,grace._fonts)
                grace.add_drawing_object(line_obj)
            else:
                MalformedPage(line)


#--------------------  Drawing Object Attributes --------------------------------------------------#
        elif draw_object_match:
            
            if line[1] == 'box':
                if line[2] == 'on' or line[1] == 'off':
                    box['onoff'] = line[2]
                elif fpat.match(line[2]):
                    box['lowleft'] = (float(line[2]),float(line[3]))
                    box['upright'] = (float(line[4]),float(line[5]))
                else:
                    if len(line) > 4:
                        attribute = "_".join(line[2:-1])
                    else:
                        attribute = line[2]
                    box[attribute] = line[-1]


            elif line[1] == 'string':
                if line[2] == 'on' or line[1] == 'off':
                    text['onoff'] = line[2]
                elif re.compile('g[0-9]+').match(line[2]):
                    pass #for now
                elif fpat.match(line[2]):
                    text['x'] = float(line[2])
                    text['y'] = float(line[3])
                elif line[2] == 'def':
                    text['text'] = quoted
                else:
                    if len(line) > 4:
                        attribute = "_".join(line[2:-1])
                    else:
                        attribute = line[2]
                    text[attribute] = line[-1]

            elif line[1] == 'line':
                if line[2] == 'on' or line[1] == 'off':
                    line_obj['onoff'] = line[2]
                elif fpat.match(line[2]):
                    line_obj['start'] = (float(line[2]),float(line[3]))
                    line_obj['end'] = (float(line[4]),float(line[5]))
                elif line[2] == 'arrow' and line[3] == 'layout':
                    line_obj['arrow_layout'] = (float(line[4]),float(line[5]))
                elif re.compile('g[0-9]+').match(line[2]):
                    pass #FOR NOW - not sure what this does
                else:
                    if len(line) > 4:
                        attribute = "_".join(line[2:-1])
                    else:
                        attribute = line[2]
                    line_obj[attribute] = line[-1]
            
#-------------------------------***READ DATASET ATTRIBUTES***------------------------------# 
        
        elif set_match and set_match.start()==0: # e.g. s0

            set = line[1]
            value = set[1:]

            # -- determine correct dataset -- #
            id = int(value)
            
            data = graph.get_dataset(id)#error checking?
            if data == None:
                data = DataSet([],grace._colors, grace._fonts)
                graph.add_dataset(data)
            
            if line[2] == 'symbol': #--read symbol--#
                if len(line) == 4:
                    data['symbol']['shape'] = line[-1]
                else:
                    if len(line) > 5:
                        attribute = line[3:-1]
                        attribute = "_".join(attribute)
                    else:
                        attribute = line[3]
                    data['symbol'][attribute] = line[-1]
                
            elif line[2] == 'line': #--read line--#
                data['line'][line[3]] = line[4]


            elif line[2] == 'dropline': #--dropline?--#
                data['dropline'] = line[3]

            elif line[2] == 'baseline': #--read baseline--#
                if line[3] == 'type':
                    data['baseline'][line[3]] = line[4]
                else:
                    try: data['baseline']['onoff'] = line[3]
                    except: MalformedPage(line)

            
            elif line[2] == 'fill': #--read fill--#
                data['fill'][line[3]] = line[4]

            elif line[2] == 'avalue': #--read avalue--#
                if line[3] in ['on','off']:
                    data['avalue']['onoff'] = line[3]
                elif line[3] == 'offset':
                    try: data['avalue']['offset'] = (float(line[4]),float(line[-1]))
                    except: MalformedPage(line)
                else:
                    attribute = None
                    if '"' in line[4]:
                        data['avalue'][line[3]] = quoted
                    else:
                        if len(line) > 4:
                            attribute = line[3:-1]
                            attribute = "_".join(attribute)
                        else:
                            attribute = line[3]
                        data['avalue'][attribute] = line[-1]

            elif line[2] == 'errorbar': #--read errorbar--#
                if line[3] in ['on','off']:
                    data['errorbar']['onoff'] = line[3]
                else:
                    if len(line) > 5:
                        attribute = line[3:-1]
                        attribute = "_".join(attribute)
                    else:
                        attribute = line[3]
                    data['errorbar'][attribute] = line[-1]

            elif line[2] in ['hidden','type','comment','legend']:
                if '"' in line[3]:
                    data[line[2]] = quoted
                else:
                    data[line[2]] = line[3]

            elif line[0] == '@target':
                pass
            else:
                MalformedPage(line)
            
#--------------------------------***READ GRAPH ATTRIBUTES***---------------------------#  
        elif line[0] == '@':

            if line[1] == 'world':    #--read world--#
                try:
                    if len(line)==6 and fpat.match(line[2]):#for newer versions
                        graph['world']['xmin'] = line[2]
                        graph['world']['ymin'] = line[3]
                        graph['world']['xmax'] = line[4]
                        graph['world']['ymax'] = line[5]
                    else:
                        graph['world'][line[2]] = line[3] #for older versions
                except:
                    MalformedPage(line)
            elif line[1] == 'stack':
                pass
            elif line[1] == 'znorm':
                graph['world']['znorm'] = line[2]

            elif line[1] == 'view':    #--read view--#
                temp = grace.get_graph(0)
                graph['view'][line[2]] = line[3]
                    
            elif line[1] == 'title':   #--read title--#
                if '"' in line[2]:
                    graph['title']['label'] = quoted
                else:
                    graph['title'][line[2]] = line[3]
                
            elif line[1] == 'subtitle':   #--read subtitle--#
                if '"' in line[2]:
                    graph['subtitle']['label'] = quoted
                else:
                    graph['subtitle'][line[2]] = line[3]

                                       #--read axis properties--#
            elif line[1] == 'xaxes' or line[1] == 'yaxes':
                if line[1] == 'xaxes':
                    graph['xaxis'][line[2]] = line[3]
                else:
                    graph['yaxis'][line[2]] = line[3]
                    
            elif line[1] == 'xaxis' or line[1] == 'yaxis':

                

                if (line[2] == 'on' or line[2] == 'off'):
                    graph[line[1]]['onoff'] = line[2]

                elif line[2] == 'type':
                    if line[3] == 'zero':
                        graph[line[1]]['type_zero'] = line[-1]
                    
                elif line[2] == 'offset':
                    try: graph[line[1]]['offset'] = (float(line[3]),float(line[-1]))
                    except: MalformedPage(line)

                elif line[2] == 'bar': #*read bar*#
                    if (line[3] == 'on' or line[3] == 'off'):
                        graph[line[1]]['bar']['onoff'] = line[3]
                    else:
                        graph[line[1]]['bar'][line[3]] = line[4]
                elif line[2] == 'label': #*read label*#
                    if '"' in line[3]:
                        graph[line[1]]['label']['label']['label'] = quoted
                    elif line[3] == 'layout':
                        graph[line[1]]['label']['layout'] = line[4]
                    elif line[3] == 'place':
                        try:
                            if fpat.match(line[4]) and fpat.match(line[-1]): #tuple type
                                graph[line[1]]['label']['place_tup'] = (float(line[4]),float(line[-1]))
                            else:
                                if line[4] == 'normal':
                                    pass #FOR NOW
                                else:
                                    graph[line[1]]['label']['place'] = line[4] #place type (normal or spec)
                        except: MalformedPage(line)
                    elif line[3] == 'char' and line[4] == 'size':
                        graph[line[1]]['label']['label']['size'] = line[5]
                    else:
                        graph[line[1]]['label']['label'][line[3]] = line[4]
                        
                elif line[2] == 'tick': #*read ticks*#
                    if (line[3] == 'on' or line[3] == 'off'):
                        graph[line[1]]['tick']['onoff'] = line[3]
                    elif (line[3] == 'in' or line[3] == 'out' or line[3] == 'both'):
                        graph[line[1]]['tick']['inout'] = line[3]
                    elif len(line) == 6 and fpat.match(line[4]):
                        graph[line[1]]['tick'].add_spec([line[3],line[4],line[5]]) #special ticks
                    else:
                        if len(line) > 5 and not fpat.match(line[4]):
                            attribute = line[3:-1]
                            attribute = "_".join(attribute)
                        else:
                            attribute = line[3]
                        graph[line[1]]['tick'][attribute] = line[-1]
                elif line[2] == 'ticklabel': #*ticklabel*#
                    if line[3] == 'offset':
                        try:
                            if fpat.match(line[4]) and fpat.match(line[-1]): #tuple type
                                graph[line[1]]['ticklabel']['offset2'] = (float(line[4]),float(line[-1]))
                            else:
                                graph[line[1]]['ticklabel']['offset1'] = line[4] #offset type (auto or spec)
                        except: MalformedPage(line)
                    elif (line[3] == 'on' or line[3] == 'off'):
                        graph[line[1]]['ticklabel']['onoff'] = line[3]
                    elif line[3] in ['formula','append','prepend'] and '"' in line[4]:
                        graph[line[1]]['ticklabel'][line[3]] = quoted
                    elif len(line) > 4 and fpat.match(line[3]):
                        graph[line[1]]['tick'].add_spec([line[2],line[3]," ".join(line[4:])])
                    else:
                        if len(line) > 5 and not fpat.match(line[3]):
                            attribute = line[3:-1]
                            attribute = "_".join(attribute)
                        else:
                            attribute = line[3]
                        graph[line[1]]['ticklabel'][attribute] = line[-1]
                           
            elif line[1] == 'legend':  #--read legend--#
                if (line[2] == 'on' or line[2] == 'off'):
                    graph['legend']['onoroff'] = line[2]
                elif line[2] == 'loctype':
                    graph['legend']['loctype'] = line[3]
                    line = file.readline()
                    line = line.replace(",","")
                    line = line.split()
                    graph['legend']['loc'] = line[2:]
                else:
                    if len(line) > 4:
                        attribute = line[2:-1]
                        attribute = "_".join(attribute)
                    else:
                        attribute = line[2]
                    graph['legend'][attribute] = line[-1]
                        
                
            elif line[1] == 'frame':   #--read frame--#
                if len(line) > 4:
                    attribute = line[2:-1]
                    attribute = "_".join(attribute)
                else:
                    attribute = line[2]
                graph['frame'][attribute] = line[-1]

                
 #-------------------------------***READ DATA SETS***-------------------------------------#    

        elif line[0] == '@target':
            while line[0] == '@target':

                target = line[1].split('.')
                graph_num = int(target[0][1:])
                data_num = int(target[1][1:])

                # -- get graph and dataset -- #
                current_graph = grace.get_graph(graph_num)     
                dataset = current_graph.get_dataset(data_num)

                
                
                line = file.readline()
                line = line.split()
                
                if not line[0] == '@type':
                    MalformedPage(line)
                type = line[1].lower()
                dataset['type'] = type
                the_data = []

                xypat = re.compile('(xy)((dy)|(dx))*', re.IGNORECASE) #ignore case
                barpat = re.compile('(bar)((dy)|(dx))*', re.IGNORECASE)
                xymatch = xypat.match(type)
                barmatch = barpat.match(type)
                
                if xymatch or barmatch \
                       or type == 'xycolor' or type == 'xycolpat'\
                       or type == 'xyhilo' \
                       or type == 'xyr' or type == 'xyz' \
                       or type == 'xyboxplot' or type == 'xyvmap' \
                       or type == 'xysize':
                       # add other types as necessary
            
                    line = file.readline()
                    line = line.split()
                    while not line[0] == '&':                    
                        try:
                            datumlist = []
                            for i in range(len(line)):
                                try: datumlist.append(float(line[i]))
                                except: datumlist.append(str(line[i]))
                            the_data.append(datumlist)
                            line = file.readline()
                            line = line.split()
                        except:
                            sys.stderr.write("ERROR READING DATA FROM THIS LINE: " + str(line) + "\n")
                            raise
                    
           
                dataset['data'] = the_data

#-----------------------------------------------------------------------------#


        elif line[0][0] == '#': # pound sign indicates comments in agr files
            pass
        else:                   # unsupported grace syntax
            sys.stderr.write( "NOT READING: " + str(line) + "\n" )
            
        line = file.readline()
        
    return grace


# =============================================================================
# =============================================================== Test function

if __name__ == '__main__':

    g = make_object()
    print g
    
    

