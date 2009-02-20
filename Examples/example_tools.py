import os

slash = os.path.sep
PYGRACE_PATH = slash.join(os.path.abspath(__file__).split(slash)[:-3])

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

    countX = countDict.items()
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

    frequencyList = countDict.items()
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
    data1 = zip(x, y1)    
    data2 = zip(x, y2)
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
            x_bar, r_bar = map(sum, zip(*window))
            moving_average.append( (x_bar / float(l), r_bar / float(l)) )
            window.pop(0)

    data1 = zip(x, y1)
    data2 = zip(x, y0)
    data3 = zip(x, r)
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
    pass

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
