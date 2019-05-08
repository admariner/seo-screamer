'''
Small class to create a Gauge with Matplotlib

Original code from
http://nicolasfauchereau.github.io/climatecode/posts/drawing-a-gauge-with-matplotlib/
https://github.com/nicolasfauchereau

He did all the work, I just created a Class out of it.

'''

from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle


class Gauge:
    def __init__(self, labels=['LOW', 'MEDIUM', 'HIGH', 'VERY HIGH', 'EXTREME'],
                 colors='jet_r', arrow=1, title='', fname=False):

        self.labels = labels
        self.colors = colors
        self.arrow = arrow
        self.title = title
        self.fname = fname

    def degree_range(self, n):
        start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
        end = np.linspace(0,180,n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return np.c_[start, end], mid_points

    def rot_text(self, ang):
        rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
        return rotation

    def gauge(self, labels=['LOW', 'MEDIUM', 'HIGH', 'VERY HIGH', 'EXTREME'],
              colors='jet_r', arrow=1, title='', fname=False):
        """
        some sanity checks first

        """

        N = len(labels)

        if arrow > N:
            raise Exception("\n\nThe category ({}) is greated than \
            the length\nof the labels ({})".format(arrow, N))

        """
        if colors is a string, we assume it's a matplotlib colormap
        and we discretize in N discrete colors 
        """

        if isinstance(colors, str):
            cmap = cm.get_cmap(colors, N)
            cmap = cmap(np.arange(N))
            colors = cmap[::-1, :].tolist()
        if isinstance(colors, list):
            if len(colors) == N:
                colors = colors[::-1]
            else:
                raise Exception("\n\nnumber of colors {} not equal \
                to number of categories{}\n".format(len(colors), N))

        """
        begins the plotting
        """

        fig, ax = plt.subplots()

        ang_range, mid_points = self.degree_range(N)

        labels = labels[::-1]

        """
        plots the sectors and the arcs
        """
        patches = []
        for ang, c in zip(ang_range, colors):
            # sectors
            patches.append(Wedge((0., 0.), .4, *ang, facecolor='w', lw=2))
            # arcs
            patches.append(Wedge((0., 0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))

        [ax.add_patch(p) for p in patches]

        """
        set the labels (e.g. 'LOW','MEDIUM',...)
        """

        for mid, lab in zip(mid_points, labels):
            ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
                    horizontalalignment='center', verticalalignment='center', fontsize=14, \
                    fontweight='bold', rotation=self.rot_text(mid))

        """
        set the bottom banner and the title
        """
        r = Rectangle((-0.4, -0.1), 0.8, 0.1, facecolor='w', lw=2)
        ax.add_patch(r)

        ax.text(0, -0.05, title, horizontalalignment='center', \
                verticalalignment='center', fontsize=22, fontweight='bold')

        """
        plots the arrow now
        """

        pos = mid_points[abs(arrow - N)]

        ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)),
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')

        ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
        ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

        """
        removes frame and ticks, and makes axis equal and tight
        """

        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        plt.tight_layout()
        if fname:
            fig.savefig(fname, dpi=200)


if __name__ == '__main__':
    g = Gauge()

    myLabels = ['75', '76', '77', '78', '79', '80', '81']
    myArrow = myLabels.index('79')+1
    g.gauge(labels=myLabels,
            colors=['#45ed08', '#8ded08', '#c3ed08', '#e9ed09', '#eda808', '#ed6308', '#ba1010'],
            arrow=myArrow, title='Just a number', fname="gauge.png")
