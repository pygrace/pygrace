#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from ..drawing_objects import DrawingObject, DrawText

__all__ = ['DrawTable']

class DrawTable(DrawingObject):
    def __init__(self, table,
                 char_size = 1.65,
                 xSpace = 0.1,
                 ySpace = 0.05,
                 color = 1,
                 font = 4,
                 lowleft = (0.5, 0.5),
                 loctype = 'view',
                 *args, **kwargs):
        DrawingObject.__init__(self, *args, **kwargs)

        multiplier = 0.03

        table.reverse()

        self.table = []
        y = lowleft[1]
        for rowIndex, row in enumerate(table):
            x = lowleft[0]
            newRow = []
            for colIndex, col in enumerate(row):
                obj = self.add_drawing_object(DrawText, text=col,
                                              char_size=char_size, x=x, y=y,
                                              color=color, font=font,
                                              loctype=loctype)
                newRow.append(obj)
                x += xSpace
            self.table.append(newRow)
            y += ySpace


if __name__ == '__main__':
    
    from random import normalvariate as nv

    from ..project import Project

    grace = Project()

    graph = grace.add_graph()

    table = [
        [r'\xm\4:', r'1.0'],
        [r'\xs\4:', r'2.0'],
        [r'\xg\4:', r'3.0'],
        ]

#     table = [(r'x', r'y')]
#     data = [('%.2f' % nv(0,1), '%.2f' % nv(0, 1)) for i in range(6)]
#     table.extend(data)

    graph.add_drawing_object(DrawTable, table, xSpace=0.15)

    graph.add_drawing_object(DrawText, text='test', loctype='world', font=59)

#     a = [(DrawText, {'text': 'Gomer'}), (DrawText, {'text': 'Spiff'})]

#     group = grace.add_drawing_object(DrawingObject)
#     group.add_drawing_object(DrawText, text='test')
#     group.add_drawing_object(DrawText, text='sdlkfj')
# #     grace.add_drawing_object(TestText, 'a')

#     grace.add_drawing_object(DrawTable, [])


    print(grace)
