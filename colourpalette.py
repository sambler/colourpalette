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

class ColourData():
    def __init__(self, r, g, b, names=[]):
        self.names = names
        # expect r,g,b to be same type?
        if type(r) == int:
            self.red = r
            self.green = g
            self.blue = b
        elif type(r) == str:
            # treat str as hex
            self.red = int(r, 16)
            self.green = int(g, 16)
            self.blue = int(b, 16)
        else:
            raise ValueError('Unknown rgb values')
        self.rgb_hex = f'#{self.red:02x}{self.green:02x}{self.blue:02x}'

    def __repr__(self):
        return self.rgb_hex

    def names(self):
        return self.names

    def rgb(self):
        return (self.red, self.green, self.blue)

    def rgb_text(self):
        return f'R: {self.red}  G: {self.green}  B: {self.blue}'

    def hsv(self):
        return cs.rgb_to_hsv(self.red, self.green, self.blue)

    def hsv_text(self):
        cv = self.hsv()
        return f'H: {cv[0]:.4f}  S: {cv[1]:.4f}  V: {cv[2]:.4f}'

    def yiq(self):
        return cs.rgb_to_yiq(self.red, self.green, self.blue)

    def yiq_text(self):
        cv = self.yiq()
        return f'Y: {cv[0]:.4f}  I: {cv[1]:.4f}  Q: {cv[2]:.4f}'

    def hls(self):
        return cs.rgb_to_hsv(self.red, self.green, self.blue)

    def hls_text(self):
        cv = self.hls()
        return f'H: {cv[0]:.4f}  L: {cv[1]:.4f}  S: {cv[2]:.4f}'

class InfoLabel(ttk.Label):
    def __init__(self, par, row, col, clipboard, sticky, **kwargs):
        super().__init__(par, **kwargs)
        self.grid(row=row, column=col, sticky=sticky, padx=PADDING, pady=PADDING)
        if clipboard is not None:
            self.clipText = clipboard
            self.bind('<Button-1>', par.do_copy)
            ToolTip(self, msg='Click to copy', follow=False, delay=0, fg=INFOTIP_FG, bg=INFOTIP_BG)

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
        colour = ColourData(int(info[0][1:-1][:2], 16),
                            int(info[0][1:-1][2:4], 16),
                            int(info[0][1:-1][4:6], 16),
                            info[1:])
        InfoLabel(self, 0, 1, colour, sticky=tk.W, width=20, background=colour)

        InfoLabel(self, 1, 0, None, sticky=tk.E, text='Names:')

        for i,ct in enumerate(info[1:]):
            InfoLabel(self, i+1, 1, ct, sticky=tk.W, text=ct)

        InfoLabel(self, 30, 0, colour, sticky=tk.E, text='HTML colour:')
        InfoLabel(self, 30, 1, colour, sticky=tk.W, text=colour)

        InfoLabel(self, 31, 0, colour.rgb(), sticky=tk.E, text='RGB:')
        InfoLabel(self, 31, 1, colour.rgb_text(), sticky=tk.W, text=colour.rgb_text())

        InfoLabel(self, 32, 0, colour.hsv(), sticky=tk.E, text='HSV:')
        InfoLabel(self, 32, 1, colour.hsv_text(), sticky=tk.W, text=colour.hsv_text())

        InfoLabel(self, 33, 0, colour.yiq(), sticky=tk.E, text='YIQ:')
        InfoLabel(self, 33, 1, colour.yiq_text(), sticky=tk.W, text=colour.yiq_text())

        InfoLabel(self, 34, 0, colour.hls(), sticky=tk.E, text='HLS:')
        InfoLabel(self, 34, 1, colour.hls_text(), sticky=tk.W, text=colour.hls_text())

    def do_copy(self, evnt):
        if evnt is not None:
            self.master.clipboard_clear()
            self.master.clipboard_append(evnt.widget.clipText)

def hsv_as_ints(inkey):
    r,b,g = int(inkey[1:3],16), int(inkey[3:5],16), int(inkey[5:7],16)
    h,s,v = cs.rgb_to_hsv(r,g,b)
    # multiply by 1000 to get a range of ints
    h = int(h*1000)
    s = int(s*1000)
    v = int(v*1000)
    return h,s,v

def sort_hsv(inkey):
    h,s,v = hsv_as_ints(inkey)
    sortkey = f'{h:04x}{s:04x}{v:04x}'
    return sortkey

class ColourPicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tk named colour palette')
        #self.geometry('500x750')
        self.TESTING = True
        self.bind('<Control-q>', lambda e: self.destroy())
        self.bind('<F5>', lambda e: self.show_colours('rgb'))
        self.bind('<F6>', lambda e: self.show_colours('hsv'))
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

    def show_colours(self, sortby='hsv'):
        """
        sortby options - rgb, hsv
        other combinations don't seem worthwhile
        """
        if hasattr(self, 'colour_grid'):
            self.colour_grid.grid_forget()
            self.colour_grid.destroy()
        self.colour_grid = ttk.Frame(self)
        self.colour_grid.grid(row=0, column=0, sticky=tk.NSEW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        if sortby == 'hsv':
            sorted_cols = sorted(self.colours, key=sort_hsv)
        else:
            # key is rgb in hex
            sorted_cols = sorted(self.colours)
        for i,c in enumerate(sorted_cols):
            row = i // NUM_COLS
            col = i % NUM_COLS
            ttip = c + ':\n' + '\n'.join(sorted(self.colours[c], key=str.lower))
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
