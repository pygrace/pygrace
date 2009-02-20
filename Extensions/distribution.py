from PyGrace.Extensions.latex_string import LatexString
from PyGrace.graph import Graph

class DistributionGraph(Graph):
    def __init__(self, data, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)
        self.dataset = self.add_dataset(data)
        self.world.ymin = 0
        self.world.xmin = 0
        self.world.xmax = 10
        self.autotick()
        xLabel = LatexString(r'\6X\f{}')
        self.xaxis.label.text = xLabel
        self.autoformat()

class CDFGraph(DistributionGraph):
    def __init__(self, data, fancy_dots, *args, **kwargs):
        DistributionGraph.__init__(self, data, *args, **kwargs)
        self.yaxis.ticklabel.configure(format="decimal",prec=1)
        self.yaxis.label.text = LatexString(r'P(\6X\f{} $\ge$ x)')

        if fancy_dots:
            self.dataset.line.configure(type=2, linestyle=0)

            # calculate position of other points, to show "real" CDF
            other = [(x0, y1) for (x0, y0), (x1, y1)
                     in zip(data[:-1], data[1:])]
            other.append((x1, 0))
            dotted = self._interlace(data, other)
            full = dotted[1:-1]

            dottedData = self.add_dataset(dotted)
            dottedData.line.configure(type=4, linestyle=2, linewidth=1)

            fullData = self.add_dataset(full)
            fullData.line.configure(type=4, linestyle=1)

            openData = self.add_dataset(other)
            openData.symbol.fill_color=0
            openData.line.linestyle=0
        else:
            self.dataset.line.configure(type=2, linestyle=1)
            self.dataset.symbol.shape = 0

    def _interlace(self, listA, listB):
        result = []
        for (a, b) in zip(listA, listB):
            result.append(a)
            result.append(b)
        return tuple(result)

class PDFGraph(DistributionGraph):
    def __init__(self, data, *args, **kwargs):
        DistributionGraph.__init__(self, data, *args, **kwargs)
        self.dataset.line.configure(type=0)
        self.dataset.dropline = 'on'
        self.autoscaley(pad=1)
        self.world.ymin = 0
        self.autotick()
        self.yaxis.label.text = LatexString(r'P(\6X\f{})')

