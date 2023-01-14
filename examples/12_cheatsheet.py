#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
from pygrace.project import Project
from pygrace.drawing_objects import DrawBox, DrawText, DrawLine, DrawEllipse

grace = Project()
graph = grace.add_graph()
graph.add_dataset([(0, 0), (1, 1)])

graph.add_drawing_object(DrawBox)
graph.add_drawing_object(DrawText)
graph.add_drawing_object(DrawLine)
graph.add_drawing_object(DrawEllipse)

grace.cheatsheet('cheatsheet.tex')

import shutil
import os
if shutil.which('pdflatex') and os.path.exists('cheatsheet.tex'):
    os.system('pdflatex cheatsheet.tex >& cheatsheet.out')

