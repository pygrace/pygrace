import sys, os, math
from grace import Grace
from graph import Graph
from dataset import DataSet

from sizeAdjust import adjust_labels

#--------------------------#
def avg(lst):
    if lst:
        sum = 0
        for num in lst:
            sum+=num
        return sum/float(len(lst))

#--------------------------#


def set_style(scale_type,grace):

    default_style(grace,scale_type)

def default_style(grace,scale_type): # For one graph, with approx. golden ratio bounding box

    grace['timestamp']['font'] = 'Helvetica'

    for graph in grace.graphs:

        #-------- Fonts --------------#

        graph['title']['font'] = 'Helvetica'
        graph['subtitle']['font'] = 'Helvetica'
        graph['legend']['font'] = 'Helvetica'
        graph['xaxis']['label']['label']['font'] = 'Helvetica'
        graph['yaxis']['label']['label']['font'] = 'Helvetica'
        graph['xaxis']['ticklabel']['font'] = 'Helvetica'
        graph['yaxis']['ticklabel']['font'] = 'Helvetica'
        graph['xaxis']['ticklabel']['char_size'] = 1.4
        graph['yaxis']['ticklabel']['char_size'] = 1.4

        #--------Tick and Frame Line Widths--------------#
        graph['frame']['linewidth'] = 2
        graph['xaxis']['bar']['linewidth'] = 2
        graph['yaxis']['bar']['linewidth'] = 2
        graph['xaxis']['tick']['major_linewidth'] = 2
        graph['yaxis']['tick']['major_linewidth'] = 2
        graph['xaxis']['tick']['minor_linewidth'] = 2
        graph['yaxis']['tick']['minor_linewidth'] = 2
        graph['legend']['box_linewidth'] = 2

        #---------Title and Axis Label Sizes----------#
        graph['title']['size'] = 2.2        
        graph['subtitle']['size'] = 1.4
        graph['xaxis']['label']['label']['size'] = 1.8
        graph['yaxis']['label']['label']['size'] = 1.8

        #----------- Data Linewidth ------------------#
        color_index = 1

        for dataset in graph.datasets:
            dataset['symbol']['char_font'] = 'Helvetica' #Dataset fonts
            dataset['avalue']['font'] = 'Helvetica'
            
            if color_index > 15: #cycle through colors for diff datasets
                color_index = 1 # restart
                
            dataset['line']['linewidth'] = 1.5
            dataset['line']['color'] = color_index 
            color_index += 1

        #-------- SCALE ------------------------------#

        scale(graph, scale_type)

        # FRAME SIZE -- Ratio of Bounding Box  sides will be approximately the golden ratio
        graph['view']['ymax'] = 0.6*(graph['view']['xmax'] - graph['view']['xmin']) + graph['view']['ymin']
        
        #---------------- Legend ---------------------#

        x = (.7*(graph['view']['xmax']-graph['view']['xmin']))+graph['view']['xmin']     
        y = (.8*(graph['view']['ymax']-graph['view']['ymin']))+graph['view']['ymin']
        
        graph['legend']['loctype'] = 'view'
        graph['legend']['loc'] = (x,y)

        
def scale(graph,type): #scaling function

    theXMax = None
    theYMax = None

    for set in graph.datasets: #Find maximum x value and maximum y value
        data = set.data
        theXMax = max(max([datum[0] for datum in data]),theXMax)
        theYMax = max(max([datum[1] for datum in data]), theYMax)

    theXMin = theXMax
    theYMin = theYMax
    yavg = []
    for set in graph.datasets: #find minimum x and minimum y values
        data = set.data
        theXMin = min(min([datum[0] for datum in data]), theXMin)
        theYMin = min(min([datum[1] for datum in data]), theYMin)
        yavg.append(avg([datum[1] for datum in data]))

    yavg = avg(yavg) # y average of all datasets

    #Origin determined by min x and min y values
    graph['world']['xmin'] = theXMin
    graph['world']['ymin'] = theYMin

    # frame edges 5% beyond max x and y value
    graph['world']['xmax'] = 1.05*(theXMax-theXMin)+theXMin
    graph['world']['ymax'] = 1.05*(theYMax-theYMin)+theYMin



    #--------------- TICK MARKS AND TICK LABELS ----------------#  -- for linear scale


    #-----------Ticklabel Precision and Format--------------#
    try:
        xrange_log = math.log10(theXMax - theXMin)
        yrange_log = math.log10(theYMax - theYMin)

        if xrange_log < 0:
            xprec = round(math.fabs(xrange_log))+1
            if xprec >= 6:
                graph['xaxis']['ticklabel']['format'] = 'Exponential'
                graph['xaxis']['ticklabel']['prec'] = 1
                graph['xaxis']['ticklabel']['skip'] = 1
            else:
                graph['xaxis']['ticklabel']['format'] = 'Decimal'
                graph['xaxis']['ticklabel']['prec'] = xprec

        if yrange_log < 0:
            yprec = round(math.fabs(yrange_log))+1
            if yprec >= 4:
                graph['yaxis']['ticklabel']['format'] = 'Exponential'
                graph['yaxis']['ticklabel']['prec'] = 1
                graph['yaxis']['ticklabel']['skip'] = 1
            else:
                graph['yaxis']['ticklabel']['format'] = 'Decimal'
                graph['yaxis']['ticklabel']['prec'] = yprec
    except: raise 
    #--------------------------------------------#


    ## sys.stderr.write(str(theYMax-theYMin) + ' diff\n')
##     sys.stderr.write(str(xrange_log) + '\n')
##     sys.stderr.write(str(yrange_log) + '\n')

    #-------------- Tick Spacing ---------------#
    
    minNumTicks = 3

    if not type == 'x' or not type == 'both':
        xtick =(10**(round(xrange_log)))/5 
        if (theXMax - theXMin)/xtick < minNumTicks:
            xtick = xtick/2
        graph['xaxis']['tick']['major'] = xtick
        graph['xaxis']['tick']['minor_ticks'] = 1
    if not type == 'y' or not type == 'both':
        ytick = (10**(round(yrange_log)))/5
        if (theYMax - theYMin)/ytick < minNumTicks:
            ytick = ytick/2
        graph['yaxis']['tick']['major'] = ytick
        graph['yaxis']['tick']['minor_ticks'] = 1

##     sys.stderr.write(str(graph['xaxis']['tick']['major']) + '\n')
##     sys.stderr.write(str(graph['yaxis']['tick']['major']) + '\n')
    
    #----------------------------------------------------------------#
    
    #------- For Log Scales -----------------------------------------#

    numMajYTicks = 5
    numMajXTicks = 8
    
    if type == 'x' or type == 'both':
        graph['xaxis']['scale'] = 'Logarithmic'
        graph['xaxis']['ticklabel']['format'] = 'Power'
        graph['xaxis']['ticklabel']['prec'] = 0
        graph['xaxis']['tick']['minor_ticks'] = 0
        if theXMin <= 0:
            raise "X DATA MUST BE > 0 FOR LOG SCALE"
        graph['xaxis']['tick']['major'] = 10**round((round(math.log10(theXMax))-round(math.log10(theXMin)))/numMajXTicks)
    if type == 'y' or type == 'both':
        graph['yaxis']['scale'] = 'Logarithmic'
        graph['yaxis']['ticklabel']['prec'] = 0
        graph['yaxis']['ticklabel']['format'] = 'Power' 
        graph['yaxis']['tick']['minor_ticks'] = 0
        if theXMin <= 0:
            raise "Y DATA MUST BE > 0 FOR LOG SCALE"
        graph['yaxis']['tick']['major'] = 10**round((round(math.log10(theYMax))-round(math.log10(theYMin)))/numMajYTicks)
        ## sys.stderr.write(str(graph['yaxis']['tick']['major']) + 'LOG\n')

