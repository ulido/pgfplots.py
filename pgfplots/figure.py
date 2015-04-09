from .util import _OptionsDict, note_pdf_encode
from .axis import Axis


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
