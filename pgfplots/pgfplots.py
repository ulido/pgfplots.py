"""pgfplots.py - A plotting library that outputs PGFPlots/LaTeX code to produce
beautiful graphs.
"""
import itertools
import collections


class _Packages(dict):
    def __str__(self):
        if len(self) == 0:
            return ""
        str_packages = []
        for k, v in self.iteritems():
            if v is None:
                str_packages.append("\usepackage{{{}}}".format(k))
            else:
                str_packages.append("\usepackage{{{}}}[{}]".format(k, v))
        return "\n".join(str_packages)


class _OptionsDict(dict):
    def __str__(self):
        if len(self) == 0:
            return ""
        str_options = []
        for k, v in self.iteritems():
            if v is None:
                str_options.append(k)
            else:
                str_options.append("{}={{{}}}".format(k, v))
        return ",".join(str_options)


class Document(object):
    """Class that describes a document consisting of one or more figures. To add
    figures call an instance's add_figure method. To get LaTeX code simply run
    str(document).
    """
    def __init__(self, classoptions={}, packages={}):
        """Initialize a new Document class instance. It is possible to specify
        options to the documentclass via the classoptions argument. Similarly,
        one can specify LaTeX packages to be loaded via the packages
        argument. Both are dict's with the key as the package name and the
        values as options (no options are indicated by a None value."""
        self.figures = []

        # Load pgfplots and pdfcomment by default
        self.packages = _Packages(packages)
        self.packages['pgfplots'] = None
        self.packages['pdfcomment'] = None

        # Use the tikz option of the standalone class by default
        self.classoptions = _OptionsDict(classoptions)
        self.classoptions['tikz'] = None

    def add_figure(self, fig):
        "Add a figure to the document."
        if not isinstance(fig, Figure):
            raise TypeError("fig needs to be of type plt.Figure")
        self.figures.append(fig)

    def __str__(self):
        figures_tex = "\n\n".join([str(fig)
                                   for fig in self.figures])
        tex = r"""\documentclass[{classoptions]{{standalone}}

{packages}
\pgfplotsset{{compat=1.10}}

\begin{{document}}
{figures}
\end{{document}}""".format(classoptions=str(self.classoptions),
                           packages=str(self.packages),
                           figures=figures_tex)

        return tex


def note_pdf_encode(note):
    "TeX-encode the given string."
    replacement = {
        "\n": r"\textLF",
        "{": r"\{",
        "}": r"\}",
        "_": r"\_",
        "&": r"\&",
        "%": r"\%",
        " ": r"~",
        }
    for k, v in replacement.iteritems():
        note = note.replace(k, v)
    return note


class Figure(object):
    """Figure class to hold a single PGF figure. To add an axis call the
    add_axes method. To produce LaTeX code, call str(figure)."""
    def __init__(self, options={}, note=None):
        """Initialize a new Figure instance. The options argument describes
        options for the corresponding tikzpicture environment (similarly to the
        classoptions argument to Document). The note argument allows one to
        include an invisible PDF comment that can be read by acroread or OS X
        Preview."""
        self.tikz_options = _OptionsDict(options)
        self.axes = []
        self.note = note

    def add_axis(self, axis):
        "Add an axis to the figure."
        if not isinstance(axis, Axis):
            raise TypeError("axis argument needs to be of type pgfplots.Axis")
        self.axes.append(axis)

    def __str__(self):
        axes_tex = "\n".join([str(ax) for ax in self.axes])
        if self.note is not None:
            note_tex = (
                "\\pdfcomment[hoffset=-1000pt,subject=Me]{{{note}}}\n".format(
                    note=note_pdf_encode(self.note)))
        else:
            note_tex = ""

        tex = r"""\begin{{tikzpicture}}[{tikz_options}]
{note_tex}{axes_tex}
\end{{tikzpicture}}""".format(note_tex=note_tex,
                              tikz_options=self.tikz_options,
                              axes_tex=axes_tex)
        return tex


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
        if not isinstance(plot, Artist):
            raise TypeError("plot argument has wrong type")
        self.plots.append(plot)

    def __str__(self):
        plots_tex = "\n".join([str(plot) for plot in self.plots])
        tex = r"""
\begin{{axis}}[{options}]
{texcode}
\end{{axis}}""".format(options=self.options, texcode=plots_tex)

        return tex


class Artist(object):
    "Base class for axis elements - needs to be subclassed."
    def __init__(self):
        raise NotImplementedError


class SimpleTeX(Artist):
    "Class to include raw LaTeX commands inside an axis environment."
    def __init__(self, texcode):
        """The texcode argument will be included verbatim inside the axis
        environment"""
        self.texcode = texcode

    def __str__(self):
        return self.texcode


class Plot(Artist):
    "Base class for plots - needs to be subclassed."
    def __init__(self):
        raise NotImplementedError


class Coordinates(object):
    """Class describing PGFPlots \addplot* coordinates to be included in a
    plotting command."""
    def __init__(self, x, y, z=None, values=None):
        """Initialize a Coordinates instance. The x and y arguments describe the
        x and y coordinates. The optional z coordinate can also be given. The
        values argument describes PGFPlots point meta values."""
        self.x = x
        self.y = y
        if not isinstance(z, collections.Iterable):
            z = len(self.x)*[z]
        self.z = z
        if not isinstance(values, collections.Iterable):
            values = len(self.x)*[values]
        self.values = values

    def __str__(self):
        c_iter = itertools.izip(self.x, self.y, self.z, self.values)
        c_strs = ("({coordinate}) [{value}]".format(
            coordinate=",".join([str(e) for e in c[:3] if e is not None]),
            value=c[3]) for c in c_iter)
        return "{"+" ".join(c_strs)+"}"


class PlotCoordinates(Plot):
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


class PlotScatter(Plot):
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

if __name__ == '__main__':
    doc = Document()
    fig = Figure(note="This is a note")
    doc.add_figure(fig)
    ax = Axis({"xlabel": "X-Axis",
               "ylabel": "Y-Axis",
               "xmin": 0,
               "xmax": 10,
               "ymin": 0,
               "ymax": 10})
    fig.add_axis(ax)
    plot = PlotCoordinates(range(10), range(10),
                           options={"color": 'green!50!black',
                                    "const plot mark mid": ""})
    ax.add_plot(plot)

    fig = Figure(note="Second note")
    doc.add_figure(fig)
    ax = Axis({"xlabel": "X-Axis",
               "ylabel": "Y-Axis",
               "xmin": 0,
               "xmax": 10,
               "ymin": 0,
               "ymax": 3,
               "zmin": 0,
               "zmax": 10,
               "grid": None})
    fig.add_axis(ax)
    plot = Plot3DConst(range(10), 2, range(9, -1, -1),
                       options={"fill": "green", "opacity": 0.5,
                                "no markers": None})
    ax.add_plot(plot)
    plot = Plot3DConst(range(10), 1, range(10),
                       options={"fill": "blue", "opacity": 0.5,
                                "no markers": None})
    ax.add_plot(plot)
    plot = PlotCoordinates(range(10), [1]*10, range(10),
                           options={"only marks": None})
    ax.add_plot(plot)
    print doc
