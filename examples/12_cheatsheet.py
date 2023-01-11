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
