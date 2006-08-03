COLUMN_WIDTH = .5

#*********************#

min_size = 1.7 #minimum character size in mm.  AIP suggests no smaller than 1.5


#********************#

##############################################################

def calc_mm(char_size, width):

    return 0.03*char_size+2.3*char_size*width-.25


def calc_char_size(mm, width):

    return (mm+.25)/(.03+2.3*width)

##############################################################

def adjust_labels(g, num_cols = 1, theMin=min_size, scale=True, IncreaseOnly=True): 

#'width' field corresponds to the width requirement in a latex figure

    width = 1.0/num_cols
    
    print "#LABEL ADJUSTMENTS:"
    min_char_size = calc_char_size(theMin,width)

    print "#min char = %s" % min_char_size
    
    sizes = []


    #--- TITLES --- #
    title = g['title']['size']
    sizes.append(title)
    subtitle =  g['subtitle']['size']
    sizes.append(subtitle)
    #---AXIS---#
    xaxis_label = g['xaxis']['label']['label']['size']
    sizes.append(xaxis_label)
    xaxis_ticklabel = g['xaxis']['ticklabel']['char_size']
    sizes.append(xaxis_ticklabel)
    yaxis_label = g['yaxis']['label']['label']['size']
    sizes.append(yaxis_label)
    yaxis_ticklabel = g['yaxis']['ticklabel']['char_size']
    sizes.append(yaxis_ticklabel)
    
    #----LEGEND---#
    legend = g['legend']['char_size']
    sizes.append(legend)

    minVal =  min(sizes)

    if(scale):  #this scales up all text to maintain ratio of char sizes

        if not IncreaseOnly or (min_char_size > minVal):
            scale = min_char_size/minVal


            
            print "#Changing title size from %s to %s" % (title,scale*title) 
            g['title']['size'] = scale*title
            print "#Changing subtitle size from %s to %s" % (subtitle,scale*subtitle) 
            g['subtitle']['size'] = scale*subtitle
            print "#Changing xaxis label from %s to %s" % (xaxis_label,scale*xaxis_label) 
            g['xaxis']['label']['label']['size'] = scale*xaxis_label
            print "#Changing yaxis label from %s to %s" % (yaxis_label,scale*yaxis_label) 
            g['yaxis']['label']['label']['size'] = scale*yaxis_label

            print "#Changing xaxis ticklabel from %s to %s" % (xaxis_ticklabel,scale*xaxis_ticklabel) 
            g['xaxis']['ticklabel']['char_size'] = scale*xaxis_ticklabel
            print "#Changing yaxis ticklabel from %s to %s" % (yaxis_ticklabel,scale*yaxis_ticklabel) 
            g['yaxis']['ticklabel']['char_size'] = scale*yaxis_ticklabel

 
            print "#Changing legend size from %s to %s" % (legend,scale*legend)
            g['legend']['char_size'] = scale*legend
        


    else:   #this only changes the character sizes which are too small
        

        print "#TITLE: %s" % title
        if(min_char_size > title):
            print "#Increasing title size from %s to %s" % (title,min_char_size) 
            g['title']['size'] = min_char_size
                        
        print "#SUBTITLE: %s" % subtitle
        if(min_char_size > subtitle):
            print "#Increasing subtitle size from %s to %s" % (subtitle,min_char_size) 
            g['subtitle']['size'] = min_char_size

        print "#xaxis: %s" % xaxis_label
        if(min_char_size > xaxis_label):
            print "#Increasing xaxis size from %s to %s" % (xaxis_label,min_char_size) 
            g['xaxis']['label']['label']['size'] = min_char_size
    
        print "#yaxis: %s" % yaxis_label
        if(min_char_size > yaxis_label):
            print "#Increasing yaxis size from %s to %s" % (yaxis_label,min_char_size) 
            g['yaxis']['label']['label']['char_size'] = min_char_size
            
        print "#xaxis: %s" % xaxis_ticklabel
        if(min_char_size > xaxis_ticklabel):
            print "#Increasing xaxis size from %s to %s" % (xaxis_ticklabel,min_char_size) 
            g['xaxis']['ticklabel']['char_size'] = min_char_size
    
        print "#yaxis: %s" % yaxis_ticklabel
        if(min_char_size > yaxis_ticklabel):
            print "#Increasing yaxis size from %s to %s" % (yaxis_ticklabel,min_char_size) 
            g['yaxis']['ticklabel']['char_size'] = min_char_size
        print "#legend: %s" % legend

        if(min_char_size > legend):
            print "#Increasing legend size from %s to %s" % (legend,min_char_size)
            g['legend']['char_size'] = min_char_size




if __name__ == '__main__':

    print calc_mm(1.8,.75)
    
    print calc_char_size(3.5, 1)

