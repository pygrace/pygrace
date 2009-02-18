import sys

# add the root directory of the PyGrace package to the PYTHONPATH
from example_tools import PYGRACE_PATH
sys.path.append(PYGRACE_PATH)

from PyGrace.grace import Grace
from PyGrace.graph import Graph
from PyGrace.drawing_objects import DrawText, DrawLine

from PyGrace.Extensions.latex_string import LatexString, CONVERT

from example_tools import output_name, calculate_cdf, calculate_pdf

class DistributionGraph(Graph):
    def __init__(self, data, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)
        self.dataset = self.add_dataset(data)
        self.autoformat()
        self.world.ymin = 0
        self.world.xmin = 0
        self.world.xmax = 10
        self.autotick()
        xLabel = LatexString(r'\6X\f{} = $\langle$ \xb\f{}\sj\N $\rangle$')
        self.xaxis.label.text = xLabel
        
class CDFGraph(DistributionGraph):
    def __init__(self, data, *args, **kwargs):
        DistributionGraph.__init__(self, data, *args, **kwargs)
        self.dataset.line.configure(type=2, linestyle=0)
        self.yaxis.ticklabel.configure(format="decimal",prec=1)
        self.yaxis.label.text = LatexString(r'P(\6X\f{} $\ge$ x)')

        # calculate position of other points, to show "real" CDF
        other = [(x0, y1) for (x0, y0), (x1, y1) in zip(data[:-1], data[1:])]
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

if __name__ == '__main__':

    # generate some data
    import random
    data = [random.randint(1, 9) for i in range(20)]
    cdf = calculate_cdf(data, normalized=True)
    pdf = calculate_pdf(data, normalized=False)

    # make the plot
    grace = Grace()

    grace.add_drawing_object(DrawText, text='Currently available LaTeX characters',
                             x=0.08, y=0.92, char_size=0.8, font=6, just=4)
    grace.add_drawing_object(DrawLine, start=(0.08, 0.915), end=(1.22, 0.915),
                             linewidth=1.0)

    mod = (len(CONVERT) / 5) + 1
    for index, (latexString, graceString) in enumerate(sorted(CONVERT.items())):
        x = 0.1 + 0.20 * (index / mod)
        y = 0.895 - 0.0225 * (index % mod)
        latexString = latexString.replace('\\', r'\\')
        grace.add_drawing_object(DrawText, text=graceString, x=x, y=y,
                                 char_size=0.6, font=4, just=1)
        grace.add_drawing_object(DrawText, text=latexString, x=x+0.01, y=y,
                                 char_size=0.6, font=4, just=0)

    grace.add_drawing_object(DrawLine,
                             start=(0.08, 0.895-0.0225*(mod-1)-0.01),
                             end=(1.22, 0.895-0.0225*(mod-1)-0.01),
                             linewidth=1.0)

    graph1 = grace.add_graph(CDFGraph, cdf)
    graph1.set_view(0.15, 0.15, 0.6, 0.6)

    graph2 = grace.add_graph(PDFGraph, pdf)
    graph2.set_view(0.75, 0.15, 1.2, 0.6)

    grace.write_file(output_name(__file__))

