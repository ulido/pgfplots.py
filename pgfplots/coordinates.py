import itertools
import collections


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
