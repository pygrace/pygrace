#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
import os

def output_name(path, extension='agr'):
    filename = os.path.abspath(path)
    try:
        base, oldExtension = filename.rsplit('.', 1)
    except ValueError:
        base = filename
    return '.'.join((base, extension))

def calculate_cdf(data, normalized=True):

    countDict = {}
    for item in data:
        try:
            countDict[item] += 1
        except KeyError:
            countDict[item]  = 1

    countX = list(countDict.items())
    countX.sort()

    unnormalized = []
    n_greater_or_equal = len(data)
    for (x, count) in countX:
        unnormalized.append( (x, n_greater_or_equal) )
        n_greater_or_equal -= count

    normalized_result = []
    for (x, n_greater_or_equal) in unnormalized:
        fraction_greater_or_equal = float(n_greater_or_equal) / len(data)
        normalized_result.append( (x, fraction_greater_or_equal) )

    if normalized:
        return normalized_result
    else:
        return unnormalized

def calculate_pdf(data, normalized=True):

    countDict = {}
    for item in data:
        try:
            countDict[item] += 1
        except KeyError:
            countDict[item]  = 1

    frequencyList = list(countDict.items())
    frequencyList.sort()

    total = float(sum(data))
    if normalized:
        return [(x, count / total) for (x, count) in frequencyList]
    else:
        return frequencyList

def singleplot():
    import math
    dn = 10
    x =  [10**(i/float(dn)) for i in range(-3*dn, 3*dn + 1)]
    y1 = [10**math.cos(math.log10(i)**2) for i in x]
    y2 = [10**math.sin(math.log10(i)**2) for i in x]
    data1 = list(zip(x, y1))    
    data2 = list(zip(x, y2))
    return data1, data2

def multiplot():
    import random
    m, b, sigma = 10, 60, 12
    x = [float(i) / 200 for i in range(0, 2000)]
    y0 = [m * x_i + b for x_i in x]
    r = [random.normalvariate(0, sigma) for i in y0]
    y1 = [y_i + r_i for y_i, r_i in zip(y0, r)]
    r_cdf = [(x_i, 1 - float(i) / len(r)) for i, x_i in enumerate(sorted(r))]
    moving_average, window, l = [], [], 100
    for x_i, r_i in zip(x, r):
        window.append((x_i, r_i))
        if len(window) >= l:
            x_bar, r_bar = list(map(sum, list(zip(*window))))
            moving_average.append( (x_bar / float(l), r_bar / float(l)) )
            window.pop(0)

    data1 = list(zip(x, y1))
    data2 = list(zip(x, y0))
    data3 = list(zip(x, r))
    data4 = moving_average
    data5 = r_cdf
    return data1, data2, data3, data4, data5

def simplesubclass():
    import random
    nv = random.normalvariate
    nSets, nPoints = 9, 200
    dataList = [[(nv(mx, 1), nv(my, 1)) for i in range(nPoints)] \
                for mx, my in [(nv(0,3), nv(0, 3)) for i in range(nSets)]]
    return dataList

def colorplot():
    from random import normalvariate
    from math import floor,ceil

    # generate some synthetic data from eliptical Gaussian
    data = []
    for i in range(10000):
        x = normalvariate(0,1.0)
        y = normalvariate(-x,1.0)
        data.append((x,y))

    # quick and dirty class for creating a pdf
    class Bin2D:
        def __init__(self,lwrbnd,uprbnd,pdf=0.0):
            self.lwrbnd = lwrbnd
            self.uprbnd = uprbnd
            self.pdf = pdf

    # create quick and dirty histogram
    delta = 0.2
    f = lambda zs: floor(min(zs)/delta)*delta
    g = lambda zs: ceil(max(zs)/delta)*delta
    xmin,ymin = list(map(f,list(zip(*data))))
    xmax,ymax = list(map(g,list(zip(*data))))
    bins = []
    for i in range(int(xmin/delta),int(xmax/delta)):
        for j in range(int(ymin/delta),int(ymax/delta)):
            lwrbnd = (i*delta,j*delta)
            uprbnd = ((i+1)*delta,(j+1)*delta)
            bins.append(Bin2D(lwrbnd,uprbnd))
    M = int(xmax/delta) - int(xmin/delta)
    N = int(ymax/delta) - int(ymin/delta)
    for datum in data:
        i = int(floor((datum[0]-xmin)/delta))
        j = int(floor((datum[1]-ymin)/delta))
        bin = bins[N*i + j]
        if not (bin.lwrbnd[0]<=datum[0] and datum[0]<bin.uprbnd[0] and
                bin.lwrbnd[1]<=datum[1] and datum[1]<bin.uprbnd[1]):
            s = "bin not correctly identified" + \
                str(bin.lwrbnd) + ' ' + str(bin.uprbnd) + ' ' + str(datum)
            raise TypeError(s)
        bin.pdf += 1.0
    minpdf,maxpdf = 1.0/float(len(data))/delta/delta, 0.0
    for bin in bins:
        bin.pdf /= float(len(data))*(bin.uprbnd[0] - bin.lwrbnd[0])\
                   *(bin.uprbnd[1] - bin.lwrbnd[1])
        if bin.pdf > maxpdf:
            maxpdf = bin.pdf

    # convert to a list of points to make this easy to understand
    data = [(bin.lwrbnd[0],bin.lwrbnd[1],
             bin.uprbnd[0],bin.uprbnd[1],
             bin.pdf) for bin in bins]
    return data

def logautoscale():
    from random import random
    data = []
    for i in range(10000):
        x = 2.0*random()-1.0
        y = 2.0*random()-1.0
        data.append((x,y))
    return data

def panels():
    import random
    dataList = []
    for i in range(9):
        data = [(random.random(), random.random()) for i in range(10)]
        dataList.append(data)
    return dataList

def latexlabels():
    import random
    data = [random.randint(1, 9) for i in range(20)]
    cdf = calculate_cdf(data, normalized=True)
    pdf = calculate_pdf(data, normalized=False)
    return cdf, pdf

def datasets():
    pass

def dataset_features():
    xs = [0.3*i for i in range(20)]
    data0 = [(x+0.0,(x+0.0)*(x+0.0)) for x in xs]
    data1 = [(x+0.1,(x+0.1)*(x+0.1)) for x in xs]
    data2 = [(x+0.2,(x+0.2)*(x+0.2)) for x in xs]
    return data0,data1,data2
   
def tree():
    newick = '((((A:1.530138801,B:1.530138801):-3.171968981e-17,((((((C:0.2525017046,D:0.2525017046):0.7637657985,E:1.016267503):0,F:1.016267503):0,(((((G:0.7977546277,H:0.7977546277):0,((I:0.7977546277,J:0.7977546277):0,K:0.7977546277):3.699839914e-17):0,L:0.7977546277):3.699839914e-17,M:0.7977546277):1.585645677e-17,N:0.7977546277):0.2185128754):0.513871298,(O:1.530138801,P:1.530138801):0):0,((((Q:0.2525017046,R:0.2525017046):0.2044491468,S:0.4569508514):8.459487451e-17,T:0.4569508514):1.07318795,(U:0.3660351673,V:0.3660351673):1.164103634):0):0):0.08608417637,(W:0.2525017046,X:0.2525017046):1.363721273):0.08465889059,(Y:0.2525017046,Z:0.2525017046):1.448380164);'
    return newick
