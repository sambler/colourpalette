#!/usr/bin/env python3

# list known colours and make a grid of swatches

# requirements
# pip install tkinter-tooltip

import colorsys as cs
import platform
import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip

NUM_COLS = 10
PADDING = 4
INFOTIP_FG = "#444444"
INFOTIP_BG = "#ffd966"

class ColourInfo(tk.Toplevel):
    """
    Show colour different ways
    click a label to copy colour that way
    """
    def __init__(self, par, coltip, **kwargs):
        super().__init__(par)
        info = coltip.split('\n')
        self.title(info[0][:-1] + ' - Info')
        self.config(padx=10, pady=10)
        r = int(info[0][1:-1][:2], 16)
        g = int(info[0][1:-1][2:4], 16)
        b = int(info[0][1:-1][4:6], 16)
        c = info[0][:-1]
        l = ttk.Label(self, text=' ', width=20, background=c)
        l.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

        l = ttk.Label(self, text='Names:')
        l.grid(row=1, column=0, sticky=tk.E, padx=5, pady=3)

        for i,ct in enumerate(info[1:]):
            l = ttk.Label(self, text=ct)
            l.grid(row=i+1, column=1, sticky=tk.W, padx=3, pady=3)
            l.clipB = ct
            l.bind('<Button-1>', self.do_copy)
            ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

        # html colour
        l = ttk.Label(self, text='HTML colour:')
        l.grid(row=10, column=0, sticky=tk.E, padx=5, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)
        l = ttk.Label(self, text=info[0])
        l.grid(row=10, column=1, sticky=tk.W, padx=3, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

        # R,G,B values
        c = f'R: {r}  G: {g}  B: {b}'
        l = ttk.Label(self, text='RGB:')
        l.grid(row=20, column=0, sticky=tk.E, padx=5, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)
        l = ttk.Label(self, text=c)
        l.grid(row=20, column=1, sticky=tk.W, padx=3, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

        # HSV values
        cv = cs.rgb_to_hsv(r,g,b)
        c = f'H: {cv[0]:.4f}  S: {cv[1]:.4f}  V: {cv[2]:.4f}'
        l = ttk.Label(self, text='HSV:')
        l.grid(row=30, column=0, sticky=tk.E, padx=5, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)
        l = ttk.Label(self, text=c)
        l.grid(row=30, column=1, sticky=tk.W, padx=3, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

        # YIQ values
        cv = cs.rgb_to_yiq(r,g,b)
        c = f'Y: {cv[0]:.4f}  I: {cv[1]:.4f}  Q: {cv[2]:.4f}'
        l = ttk.Label(self, text='YIQ:')
        l.clipB = c
        l.grid(row=40, column=0, sticky=tk.E, padx=5, pady=3)
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)
        l = ttk.Label(self, text=c)
        l.clipB = c
        l.grid(row=40, column=1, sticky=tk.W, padx=3, pady=3)
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

        # HLS values
        cv = cs.rgb_to_hsv(r,g,b)
        c = f'H: {cv[0]:.4f}  L: {cv[1]:.4f}  S: {cv[2]:.4f}'
        l = ttk.Label(self, text='HLS:')
        l.grid(row=50, column=0, sticky=tk.E, padx=5, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)
        l = ttk.Label(self, text=c)
        l.grid(row=50, column=1, sticky=tk.W, padx=3, pady=3)
        l.clipB = c
        l.bind('<Button-1>', self.do_copy)
        ToolTip(l, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

    def do_copy(self, evnt):
        if evnt is not None:
            self.master.clipboard_clear()
            self.master.clipboard_append(evnt.widget.clipB)


class ColourPicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tk named colour palette')
        #self.geometry('500x750')
        self.TESTING = True
        self.bind('<Control-q>', lambda e: self.destroy())
        self.read_colours()
        self.show_colours()

    def read_colours(self):
        # python used the X11 rgb.txt for colour names
        # get list of colours defined in rgb.txt
        if platform.system() == 'FreeBSD':
            RGBFILE = '/usr/local/lib/X11/rgb.txt'
        elif platform.system() == 'Linux':
            RGBFILE = '/usr/share/X11/rgb.txt' # accurate??
        elif platform.system() == 'Windows':
            RGBFILE = 'where is this??'
        with open(RGBFILE, 'r') as cf:
            cfdata = cf.read()
            self.all_colours = sorted([l for l in cfdata.split('\n')])

        if self.all_colours[0] == '':
            del self.all_colours[0] # remove empty first line

        self.colours = {}
        # make dict of colour values listing names
        for c in self.all_colours:
            cl = c.split()
            colour = f'#{int(cl[0]):02x}{int(cl[1]):02x}{int(cl[2]):02x}'
            if colour not in self.colours:
                self.colours[colour] = set()
            self.colours[colour].add(cl[3])

    def show_colours(self, sortby='html'):
        """
        TODO add sort buttons to top of window
        sortby options -
        html = alpha by html hex value (same as rgb)
        TODO [rgb] = red,green,blue values (TODO in order listed)
        TODO [hsv] = hue,saturation,value (TODO in order listed)
        """
        if hasattr(self, 'colour_grid'):
            self.colour_grid.grid_forget()
            self.colour_grid.destroy()
        self.colour_grid = ttk.Frame(self)
        self.colour_grid.grid(row=0, column=0, sticky=tk.NSEW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # TODO sort here
        sorted_cols = sorted(self.colours)
        for i,c in enumerate(sorted_cols):
            row = i // NUM_COLS
            col = i % NUM_COLS
            ttip = c + ':\n' + '\n'.join(sorted(self.colours[c]))
            lbl = ttk.Label(self.colour_grid, text=' ', background=c, width=8)
            lbl.coltip = ttip
            lbl.grid(row=row, column=col, sticky=tk.NSEW)
            lbl.bind('<Button-1>', self.copy_colour)
            lbl.bind('<Button-3>', self.colour_info)
            ToolTip(lbl, msg=ttip+'\n\nClick to copy #hex\nRight-click for details', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)
        # show colour count
        r = len(self.colours)
        lbl = ttk.Label(self.colour_grid, text=str(r))
        lbl.grid(row=r+1, column=NUM_COLS-1)

    def copy_colour(self, evnt=None):
        if evnt is None: return
        info = evnt.widget.coltip
        self.clipboard_clear()
        self.clipboard_append(info.split('\n')[0][:-1]) # copy html style value

    def colour_info(self, evnt=None):
        if evnt is None: return
        w = ColourInfo(self, evnt.widget.coltip)

    def main(self, args=None):
        return self.mainloop()

def main():
    # point setup.entry_points here
    import sys
    mw = ColourPicker()
    mw.TESTING = '--debug' in sys.argv
    sys.exit(mw.main(sys.argv))

if __name__ == '__main__':
    main()
