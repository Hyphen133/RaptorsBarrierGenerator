import matplotlib.pyplot as plt

def show_polygon(polygon, show=True):
    x, y = polygon.exterior.xy
    plt.plot(x, y)

    if show:
        plt.show()

def show_line(line, show=True):
    x, y = line.xy
    plt.plot(x, y)

    if show:
        plt.show()

def show_geometry(geometry, show = True):
    show_polygon(geometry.internal, show=False)
    show_polygon(geometry.external, show=False)

    if show:
        plt.show()