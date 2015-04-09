import pgfplots as pgf


if __name__ == '__main__':
    doc = pgf.Document()
    fig = pgf.Figure(note="This is a note")
    doc.add_figure(fig)
    ax = pgf.Axis({"xlabel": "X-Axis",
                   "ylabel": "Y-Axis",
                   "xmin": 0,
                   "xmax": 10,
                   "ymin": 0,
                   "ymax": 10})
    fig.add_axis(ax)
    plot = pgf.PlotCoordinates(range(10), range(10),
                               options={"color": 'green!50!black',
                                        "const plot mark mid": ""})
    ax.add_plot(plot)

    fig = pgf.Figure(note="Second note")
    doc.add_figure(fig)
    ax = pgf.Axis({"xlabel": "X-Axis",
                   "ylabel": "Y-Axis",
                   "xmin": 0,
                   "xmax": 10,
                   "ymin": 0,
                   "ymax": 3,
                   "zmin": 0,
                   "zmax": 10,
                   "grid": None})
    fig.add_axis(ax)
    plot = pgf.Plot3DConst(range(10), 2, range(9, -1, -1),
                           options={"fill": "green", "opacity": 0.5,
                                    "no markers": None})
    ax.add_plot(plot)
    plot = pgf.Plot3DConst(range(10), 1, range(10),
                           options={"fill": "blue", "opacity": 0.5,
                                    "no markers": None})
    ax.add_plot(plot)
    plot = pgf.PlotCoordinates(range(10), [1]*10, range(10),
                               options={"only marks": None})
    ax.add_plot(plot)

    print doc
