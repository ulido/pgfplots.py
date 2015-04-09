"""pgfplots.py - A plotting library that outputs PGFPlots/LaTeX code to produce
beautiful graphs.
"""
from .document import Document
from .figure import Figure
from .axis import Axis
from .plot import SimpleTeX
from .plot import PlotBase, PlotCoordinates, PlotScatter, Plot3DConst
from .coordinates import Coordinates
from .util import note_pdf_encode

__all__ = [
    'Document',
    'Figure',
    'Axis',
    'SimpleTeX', 'PlotBase', 'PlotCoordinates', 'PlotScatter', 'Plot3DConst',
    'Coordinates',
    'note_pdf_encode',
    ]
