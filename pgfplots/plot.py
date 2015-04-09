from .util import _OptionsDict
from .coordinates import Coordinates

import itertools


class PlotBase(object):
    "Base class for axis elements - needs to be subclassed."
    def __init__(self):
        raise NotImplementedError


class SimpleTeX(PlotBase):
    "Class to include raw LaTeX commands inside an axis environment."
    def __init__(self, texcode):
        """The texcode argument will be included verbatim inside the axis
        environment"""
        self.texcode = texcode

    def __str__(self):
        return self.texcode


class PlotCoordinates(PlotBase):
    """Class describing a simple \addplots with inline coordinates."""
    def __init__(self, x, y, z=None,
                 options={}, use_cycle=True, label=None):
        """Initialize a new PlotCoordinates instance. The x, y and (optional) z
        arguments are sequences describing the xyz coordinates of the plot. If z
        is given the plotting command is automatically turned into an \addplot3
        command. The options argument allows one to specify options to the
        addplots command. use_cycle allows for the addition of the + to
        \addplots and the label argument includes an \addlegend{label} command."""
        self.options = _OptionsDict(options)
        self.label = label
        if use_cycle:
            self._plus = "+"
        else:
            self._plus = ""
        if z is not None:
            self.threed = "3"
        else:
            self.threed = ""

        self.coordinates = Coordinates(x, y, z)

    def __str__(self):
        if self.label is None:
            label = ""
        else:
            label = "\addlegendentry{{{}}}".format(self.label)
        return r"""\addplot{threed}{plus}[{options}] coordinates {coordinates};
        {label}""".format(
            threed=self.threed,
            plus=self._plus,
            options=self.options,
            coordinates=self.coordinates,
            label=label)


class PlotScatter(PlotBase):
    def __init__(self, x, y, values=None,
                 options={}, use_cycle=True, label=None):
        self.options = _OptionsDict(options)
        self.options["scatter"] = None
        self.options["scatter src"] = "explicit"
        self.options["only marks"] = None
        self.label = label
        if use_cycle:
            self._plus = "+"
        else:
            self._plus = ""
        self.values = values
        
        self.coordinates = Coordinates(x, y, values=values)

    def __str__(self):
        if self.label is None:
            label = ""
        else:
            label = "\addlegendentry{{{}}}".format(self.label)
        return r"""\addplot{plus}[{options}] coordinates {coordinates};
        {label}""".format(
            plus=self._plus,
            options=self.options,
            coordinates=self.coordinates,
            label=label)


class Plot3DConst(PlotCoordinates):
    def __init__(self, x, ylevel, z, options={}, use_cycle=True, label=None):
        x, y, z = self._fix_3d_const_plot(x, ylevel, z)
        PlotCoordinates.__init__(self, x, y, z,
                                 options, use_cycle, label)

    def _fix_3d_const_plot(self, x, ylevel, z):
        c_iter = itertools.izip(x, z)
        lx, lz = next(c_iter)

        rx, rz = [lx, lx], [0, lz]
        for px, pz, in c_iter:
            dx = px-lx
            rx.extend(2*[lx+dx/2.0])
            rz.extend([lz, pz])
            lx, lz = px, pz
        rx.extend(2*[lx+dx/2.0])
        rz.extend([lz, 0])

        return rx, [ylevel]*len(rx), rz



