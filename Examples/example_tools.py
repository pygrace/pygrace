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

