from .util import _OptionsDict
from .plot import PlotBase


class Axis(object):
    """Axis class to describe a single axis in a figure (corresponding to a
    PGFPlots axis environment. To add plots (\addplots* commands) call the
    add_plot method. To produce corresponding LaTeX output call str(axis)."""
    def __init__(self, options={}):
        """Initialize a new axis environment. The options argument allows one to
        specify options to the axis environment."""
        self.options = _OptionsDict(options)
        self.plots = []

    def add_plot(self, plot):
        "Add a new plot to the axis."
        if not isinstance(plot, PlotBase):
            raise TypeError("plot argument has wrong type")
        self.plots.append(plot)

    def __str__(self):
        plots_tex = "\n".join([str(plot) for plot in self.plots])
        tex = r"""
\begin{{axis}}[{options}]
{texcode}
\end{{axis}}""".format(options=self.options, texcode=plots_tex)

        return tex
