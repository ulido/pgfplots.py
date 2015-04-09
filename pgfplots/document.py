from .util import _Packages, _OptionsDict
from .figure import Figure


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
        tex = r"""\documentclass[{classoptions}]{{standalone}}

{packages}
\pgfplotsset{{compat=1.10}}

\begin{{document}}
{figures}
\end{{document}}""".format(classoptions=str(self.classoptions),
                           packages=str(self.packages),
                           figures=figures_tex)

        return tex
