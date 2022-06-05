#! /usr/bin/python3
'''
Copyright (C) 2022 Christian Hoffmann christian@lehrer-hoffmann.de

## This Extension converts the endpoints of a path into a csv-string.
## Select the path and a rectangle. Set the values for x-min, x-max,
## y-min and y-max in the extension. You will receive a csv-string 
## with respect to the values of the rectangle.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from inkex import EffectExtension, PathElement, Rectangle, errormsg


class Path_To_X_Y(EffectExtension):
    def __init__(self):
        super().__init__()
        self.arg_parser.add_argument("--tab")
        self.arg_parser.add_argument("--x_min", dest="x_min", action="store", type=float, default=0)
        self.arg_parser.add_argument("--x_max", dest="x_max", action="store", type=float, default=1)
        self.arg_parser.add_argument("--y_min", dest="y_min", action="store", type=float, default=0)
        self.arg_parser.add_argument("--y_max", dest="y_max", action="store", type=float, default=1)
        self.arg_parser.add_argument("--csv_delimiter", dest="csv_delimiter", action="store", type=str, default=";")
        self.arg_parser.add_argument("--x_format", dest="x_format", action="store", type=str, default="9.4f")
        self.arg_parser.add_argument("--y_format", dest="y_format", action="store", type=str, default="9.4f")

    def rechteck_koordinate(self, v, achse):
        min = self.rechteck.left
        max = self.rechteck.right
        if achse == 'y':
            min = self.rechteck.bottom
            max = self.rechteck.top
        return (v-min)/(max-min)

    def wert_koordinate(self, v, achse):
        min = self.options.x_min
        max = self.options.x_max
        if achse == 'y':
            min = self.options.y_min
            max = self.options.y_max
        return (max-min)*v+min

    def effect(self):
        xystring = ''
        if self.options.y_min == self.options.y_max:
            errormsg(_('y_min and y_max must not be equal.'))
        if self.options.x_min == self.options.x_max:
            errormsg('x_min and x_max must not be equal.')


        pfade = self.svg.selection.filter(PathElement)
        rechtecke = self.svg.selection.filter(Rectangle)
        if len(pfade) != 1 or len(rechtecke) != 1:
            errormsg(_('Please select exactly one path and one rectangle (Shift-Click).'))
            return
        self.pfad = pfade[0]
        self.rechteck = rechtecke[0]

        if self.rechteck.top == self.rechteck.bottom:
            errormsg(_('The rectangle height must not be zero.'))
            return
        if self.rechteck.left == self.rechteck.right:
            errormsg(_('The rectangle width must not be zero.'))
            return

        for p in self.pfad.path.end_points:
            rx = self.rechteck_koordinate(p.x, 'x')
            ry = self.rechteck_koordinate(p.y, 'y')
            vx = self.wert_koordinate(rx, 'x')
            vy = self.wert_koordinate(ry, 'y')
            xystring += f'{vx:{self.options.x_format}}{self.options.csv_delimiter}{vy:{self.options.y_format}}\n'
        errormsg(xystring)


if __name__ == '__main__':
    e = Path_To_X_Y()
    e.run()
