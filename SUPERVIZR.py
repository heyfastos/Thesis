__author__ = 'steffen'

import argparse
import numpy as np
from enum import Enum
from math import fabs, log2, log10, log, pow, exp
import textwrap
import matplotlib.pyplot as plt

class Color(Enum):
    blue = 0
    pink = 1
    green = 2
    grey = 3
    red = 4
    yellow = 5
    purple = 6
    orange = 7
    dark_grey = 8

class RowCol(Enum):
    row = 0
    col = 1

# DESCRIPTION: Computes one element with border, scaling and bars
# INPUT:
#   - pos_x <int> : grid position i (x-axis)
#   - pos_y <int> : grid position j (y-axis)
#   - abs_max_value <float> : |max_Value| is needed for scaling
#   - val_hash <dict[Color.i]> : contains the bar value for each color (sub columns)
#   - scaling=73 <float> : global scaling
#   - offset_x=0 <float> : global offset for canvas_x
#   - offset_y=0 <float> : global offset for canvas_y
# OUTPUT: str(<Element>) => HTML-Code
class Element:
    def __init__(self, pos_x, pos_y, abs_max_value, val_hash, scaling=73, offset_x=0, offset_y=0):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__abs_max_value = abs_max_value
        self.__scaling = scaling
        self.__num_members = len(val_hash)
        self.__val_hash = val_hash
        self.__offset_x = offset_x
        self.__offset_y = offset_y
        self.__colors()
        self.__compute_diameter()

    def __colors(self):
        # [blue,red,green,yellow,pink,purple]
        self.colors = dict()
        self.colors_gradient_lookup = dict()
        # blue
        self.colors[Color.blue] = "#0044FF"
        color_light_dark = ["#8ED6FF", "#004CB3"]
        self.colors_gradient_lookup[Color.blue] = list()
        self.colors_gradient_lookup[Color.blue].append(color_light_dark)
        # red
        self.colors[Color.red] = "#FF0000"
        color_light_dark = ["#FF9090", "#B30006"]
        self.colors_gradient_lookup[Color.red] = list()
        self.colors_gradient_lookup[Color.red].append(color_light_dark)
        # green
        self.colors[Color.green] = "#08A105"
        color_light_dark = ["#90FF9B", "#00B306"]
        self.colors_gradient_lookup[Color.green] = list()
        self.colors_gradient_lookup[Color.green].append(color_light_dark)
        # yellow
        self.colors[Color.yellow] = "#FCFF00"
        color_light_dark = ["#FFFC90", "#B0B300"]
        self.colors_gradient_lookup[Color.yellow] = list()
        self.colors_gradient_lookup[Color.yellow].append(color_light_dark)
        # pink
        self.colors[Color.pink] = "#FF00D5"
        color_light_dark = ["#FF90E6", "#B300A4"]
        self.colors_gradient_lookup[Color.pink] = list()
        self.colors_gradient_lookup[Color.pink].append(color_light_dark)
        # purple
        self.colors[Color.purple] = "#8D00FF"
        color_light_dark = ["#D190FF", "#8600B3"]
        self.colors_gradient_lookup[Color.purple] = list()
        self.colors_gradient_lookup[Color.purple].append(color_light_dark)
        # orange
        self.colors[Color.orange] = "#FFD500"
        color_light_dark = ["#FFEA7C", "#E7C101"]
        self.colors_gradient_lookup[Color.orange] = list()
        self.colors_gradient_lookup[Color.orange].append(color_light_dark)
        # grey
        self.colors[Color.grey] = "#737171"
        color_light_dark = ["#DBD9D9", "#6B6B6B"]
        self.colors_gradient_lookup[Color.grey] = list()
        self.colors_gradient_lookup[Color.grey].append(color_light_dark)
        # black
        self.colors[Color.dark_grey] = "#575656"
        color_light_dark = ["#AAA8A8", "#353535"]
        self.colors_gradient_lookup[Color.dark_grey] = list()
        self.colors_gradient_lookup[Color.dark_grey].append(color_light_dark)

    def __compute_diameter(self):
        coord_x_start = 0
        coord_y_start = 0
        coord_x_end = 1
        coord_y_end = 1
        grid_offset_x = self.__pos_x * self.__scaling
        grid_offset_y = self.__pos_y * self.__scaling
        # add center line (x-axis)
        self.__center_line = dict()
        self.__center_line["x_start"] = self.__offset_x + float(self.__scaling * (coord_x_start)) + grid_offset_x
        self.__center_line["y_start"] = self.__offset_y + float(self.__scaling * (coord_y_end / 2)) + grid_offset_y
        self.__center_line["x_end"] = self.__offset_x + float(self.__scaling * (coord_x_end)) + grid_offset_x
        self.__center_line["y_end"] = self.__offset_y + float(self.__scaling * (coord_y_end / 2)) + grid_offset_y
        self.__center_line["width"] = 0.5
        self.__center_line["color"] = self.colors_gradient_lookup[Color.dark_grey][0][0]
        # add frame
        self.__main_frame = dict()
        self.__main_frame["x_start"] = self.__offset_x + float(self.__scaling * (coord_x_start)) + grid_offset_x
        self.__main_frame["y_start"] = self.__offset_y + float(self.__scaling * (coord_y_start)) + grid_offset_y
        self.__main_frame["x_shift"] = float(self.__scaling * (coord_x_end))
        self.__main_frame["y_shift"] = float(self.__scaling * (coord_y_end))
        self.__main_frame["width"] = 1.5
        self.__main_frame["color"] = self.colors_gradient_lookup[Color.dark_grey][0][0]
        # add bars
        self.__bars = list()
        count = 0
        for key_color in Color:
            if key_color in self.__val_hash:
                scaled_value_y = self.__val_hash[key_color]
                bar_offset = self.__main_frame["x_shift"] / self.__num_members
                bars = dict()
                bars["x_start"] = self.__center_line["x_start"] + (bar_offset/2) + (count * bar_offset)
                bars["y_start"] = float(self.__center_line["y_start"])
                bars["x_end"] = self.__center_line["x_start"] + (bar_offset/2) + (count * bar_offset)
                bars["y_end"] = float(self.__center_line["y_start"]) - float((scaled_value_y * (self.__main_frame["y_shift"]/2)) / self.__abs_max_value)
                bars["width"] = bar_offset
                if bars["y_end"] < self.__center_line["y_start"]:
                    bars["color"] = self.colors_gradient_lookup[key_color][0][0]
                else:
                    bars["color"] = self.colors_gradient_lookup[key_color][0][1]
                self.__bars.append(bars)
                count += 1

    def __generate_coord_system_html(self):
        frame_html = "context.beginPath();\n"
        frame_html += "context.moveTo(" + str(self.__center_line["x_start"]) + "," + str(self.__center_line["y_start"]) + ");\n"
        frame_html += "context.lineTo(" + str(self.__center_line["x_end"]) + "," + str(self.__center_line["y_end"]) + ");\n"
        frame_html += "context.lineWidth = " + str(self.__center_line["width"]) + ";\n"
        frame_html += "context.strokeStyle = '" + str(self.__center_line["color"]) + "';\n"
        frame_html += "context.stroke();\n"
        return frame_html

    def __generate_bar_html(self):
        frame_html = ""
        for hash_i in self.__bars:
            frame_html += "context.beginPath();\n"
            frame_html += "context.moveTo(" + str(hash_i["x_start"]) + "," + str(hash_i["y_start"]) + ");\n"
            frame_html += "context.lineTo(" + str(hash_i["x_end"]) + "," + str(hash_i["y_end"]) + ");\n"
            frame_html += "context.lineWidth = " + str(hash_i["width"]) + ";\n"
            frame_html += "context.strokeStyle = '" + str(hash_i["color"]) + "';\n"
            frame_html += "context.stroke();\n"
        return frame_html

    def __generate_frame_html(self):
        frame_html = "context.beginPath();\n"
        frame_html += "context.rect(" + str(self.__main_frame["x_start"]) + "," + str(self.__main_frame["y_start"]) + \
                                  "," + str(self.__main_frame["x_shift"]) + "," + str(self.__main_frame["y_shift"]) + ");\n"
        frame_html += "context.lineWidth = " + str(self.__main_frame["width"]) + ";\n"
        frame_html += "context.strokeStyle = '" + str(self.__main_frame["color"]) + "';\n"
        frame_html += "context.stroke();\n"
        return frame_html

    def __generate_html_code(self):
        coord = self.__generate_coord_system_html()
        bars = self.__generate_bar_html()
        frame = self.__generate_frame_html()
        return (str(coord) + str(bars) + str(frame))

    def __str__(self):
        return self.__generate_html_code()

# DESCRIPTION: Computes an y-axis for each end-element (last plot in a row)
# INPUT:
#   - col_abs <int> : #{col} to get x coordinates
#   - row_num <int> : to compute a coordinate system for each row
#   - abs_max_value <float> : |max_Value| is needed for scaling
#   - scaling=73 <float> : global scaling
#   - offset_x=0 <float> : global offset for canvas_x
#   - offset_y=0 <float> : global offset for canvas_y
# OUTPUT: str(<Scale>) => HTML-Code
class Scale:
    def __init__(self, col_abs, row_num, abs_max_value, scaling=73, offset_x=0, offset_y=0):
        self.__col_abs = col_abs
        self.__row_num = row_num
        self.__max_value = abs_max_value
        self.__scaling = scaling
        self.__offset_x = offset_x
        self.__offset_y = offset_y
        self.__colors()
        self.__compute_diameter()

    def __colors(self):
        # [blue,red,green,yellow,pink,purple]
        self.colors = dict()
        self.colors_gradient_lookup = dict()
        # blue
        self.colors[Color.blue] = "#0044FF"
        color_light_dark = ["#8ED6FF", "#004CB3"]
        self.colors_gradient_lookup[Color.blue] = list()
        self.colors_gradient_lookup[Color.blue].append(color_light_dark)
        # red
        self.colors[Color.red] = "#FF0000"
        color_light_dark = ["#FF9090", "#B30006"]
        self.colors_gradient_lookup[Color.red] = list()
        self.colors_gradient_lookup[Color.red].append(color_light_dark)
        # green
        self.colors[Color.green] = "#08A105"
        color_light_dark = ["#90FF9B", "#00B306"]
        self.colors_gradient_lookup[Color.green] = list()
        self.colors_gradient_lookup[Color.green].append(color_light_dark)
        # yellow
        self.colors[Color.yellow] = "#FCFF00"
        color_light_dark = ["#FFFC90", "#B0B300"]
        self.colors_gradient_lookup[Color.yellow] = list()
        self.colors_gradient_lookup[Color.yellow].append(color_light_dark)
        # pink
        self.colors[Color.pink] = "#FF00D5"
        color_light_dark = ["#FF90E6", "#B300A4"]
        self.colors_gradient_lookup[Color.pink] = list()
        self.colors_gradient_lookup[Color.pink].append(color_light_dark)
        # purple
        self.colors[Color.purple] = "#8D00FF"
        color_light_dark = ["#D190FF", "#8600B3"]
        self.colors_gradient_lookup[Color.purple] = list()
        self.colors_gradient_lookup[Color.purple].append(color_light_dark)
        # orange
        self.colors[Color.orange] = "#FFD500"
        color_light_dark = ["#FFEA7C", "#E7C101"]
        self.colors_gradient_lookup[Color.orange] = list()
        self.colors_gradient_lookup[Color.orange].append(color_light_dark)
        # grey
        self.colors[Color.grey] = "#737171"
        color_light_dark = ["#DBD9D9", "#6B6B6B"]
        self.colors_gradient_lookup[Color.grey] = list()
        self.colors_gradient_lookup[Color.grey].append(color_light_dark)
        # dark_grey
        self.colors[Color.dark_grey] = "#575656"
        color_light_dark = ["#AAA8A8", "#353535"]
        self.colors_gradient_lookup[Color.dark_grey] = list()
        self.colors_gradient_lookup[Color.dark_grey].append(color_light_dark)

    def __compute_diameter(self):
        color = self.colors[Color.dark_grey]
        self.line_with = 1
        # compute vertical line suitable to the corresponding row
        self.__line_x_start = self.__offset_x + 3 + (self.__col_abs * self.__scaling)
        self.__line_y_start = self.__offset_y + (self.__row_num * self.__scaling) + 1
        self.__line_x_end = self.__offset_x + 3 + (self.__col_abs * self.__scaling)
        self.__line_y_end = self.__offset_y + (self.__row_num * self.__scaling) + self.__scaling - 1
        self.__line_color = color
        # compute list of ticks (depending on scaling)
        center_x = self.__line_x_start
        center_y = self.__line_y_end - ((self.__line_y_end - self.__line_y_start) / 2)
        tick_length = 2
        num_of_ticks = 3
        value_step = self.__max_value / num_of_ticks
        tick_range = (((self.__line_y_end - self.__line_y_start) / 2) / num_of_ticks)
        self.__tick_list = list()
        for i in range(1, num_of_ticks):
            tick_value = (value_step * i)
            # plus range -y
            tick_x_start = center_x
            tick_y_start = center_y - (tick_range * i)
            tick_x_end = center_x + tick_length
            tick_y_end = center_y - (tick_range * i)
            self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round(tick_value, 1)])
            # minus range +y
            tick_y_start = center_y + (tick_range * i)
            tick_y_end = center_y + (tick_range * i)
            self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round(((-1) * tick_value), 1)])
        # add center tick
        tick_x_start = center_x
        tick_y_start = center_y
        tick_x_end = center_x + tick_length + 3
        tick_y_end = center_y
        self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, 0])
        # add end ticks
        tick_x_start = self.__line_x_start
        tick_y_start = self.__line_y_start
        tick_x_end = self.__line_x_start + tick_length + 3
        tick_y_end = self.__line_y_start
        self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round(self.__max_value, 1)])
        tick_x_start = self.__line_x_end
        tick_y_start = self.__line_y_end
        tick_x_end = self.__line_x_end + tick_length + 3
        tick_y_end = self.__line_y_end
        self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round(((-1) * self.__max_value), 1)])

    def __generate_numbers_html(self):
        frame_html = ""
        count = 0
        max_count_center = len(self.__tick_list) - 3
        max_count_start_tick = len(self.__tick_list) - 2
        max_count_end_tick = len(self.__tick_list) - 1
        letter_size = float(self.__scaling * (1 / 10))
        letter_size_2 = float(self.__scaling * (1 / 11.5))
        scaling_top = int(self.__scaling * (1 / 12)) #(180 -> 12)
        scaling_normal = int(self.__scaling * (1 / 30)) #(180 -> 6)
        scaling_up = int(self.__scaling * (1 / 65)) #(180 -> 3)
        for sub_arr in self.__tick_list:
            frame_html += "context.fillStyle = '" + str(self.colors_gradient_lookup[Color.dark_grey][0][1]) + "';\n"
            frame_html += "context.textAlign = 'left';\n"
            if count == max_count_start_tick:
                frame_html += "context.font = 'bold " + str(letter_size) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0] + 7) + "," + str((sub_arr[3] + scaling_top)) + ");\n"
            elif count == max_count_end_tick:
                frame_html += "context.font = 'bold " + str(letter_size) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0] + 7) + "," + str((sub_arr[3] - scaling_up)) + ");\n"
            elif count == max_count_center:
                frame_html += "context.font = 'bold " + str(letter_size) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0] + 7) + "," + str((sub_arr[3] + scaling_normal)) + ");\n"
            else:
                frame_html += "context.font = 'italic " + str(letter_size_2) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0] + 7) + "," + str((sub_arr[3] + scaling_normal)) + ");\n"
            count += 1
        return frame_html

    def __generate_ticks_html(self):
        frame_html = ""
        for sub_arr in self.__tick_list:
            frame_html += "context.beginPath();\n"
            frame_html += "context.moveTo(" + str(sub_arr[0]) + "," + str(sub_arr[1]) + ");\n"
            frame_html += "context.lineTo(" + str(sub_arr[2]) + "," + str(sub_arr[3]) + ");\n"
            frame_html += "context.lineWidth = " + str(self.line_with) + ";\n"
            frame_html += "context.strokeStyle = '" + str(self.__line_color) + "';\n"
            frame_html += "context.stroke();\n"
        return frame_html

    def __generate_scale_html(self):
        #line_width = 1
        frame_html = "context.beginPath();\n"
        frame_html += "context.moveTo(" + str(self.__line_x_start) + "," + str(self.__line_y_start) + ");\n"
        frame_html += "context.lineTo(" + str(self.__line_x_end) + "," + str(self.__line_y_end) + ");\n"
        frame_html += "context.lineWidth = " + str(self.line_with) + ";\n"
        frame_html += "context.strokeStyle = '" + str(self.__line_color) + "';\n"
        frame_html += "context.stroke();\n"
        return frame_html

    def __generate_html_code(self):
        numbers = self.__generate_numbers_html()
        ticks = self.__generate_ticks_html()
        scale = self.__generate_scale_html()
        return (str(scale) + str(ticks) + str(numbers))

    def __str__(self):
        return self.__generate_html_code()

# DESCRIPTION: Computes position for row or column labels; labels will be automatically increase or decrease
# INPUT:
#   - row_or_col <string>[row,col]: select row or column what you prefere to annotate
#   - pos_x : grid position i (x-axis)
#   - pos_y :grid position i (y-axis)
#   - label <string> : label name
#   - scaling=73 <float> : global scaling
#   - offset_x=0 <float> : global offset for canvas_x
#   - offset_y=0 <float> : global offset for canvas_y
# OUTPUT: str(<Label>) => HTML-Code
class Label:
    def __init__(self, row_or_col, pos_x, pos_y, label, scaling=73, offset_x=0, offset_y=0):
        self.__row_or_col = row_or_col
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__label = label
        self.__scaling = scaling
        self.__offset_x = offset_x
        self.__offset_y = offset_y
        self.__colors()

    def __colors(self):
        # [blue,red,green,yellow,pink,purple]
        self.colors = dict()
        self.colors_gradient_lookup = dict()
        # blue
        self.colors[Color.blue] = "#0044FF"
        color_light_dark = ["#8ED6FF", "#004CB3"]
        self.colors_gradient_lookup[Color.blue] = list()
        self.colors_gradient_lookup[Color.blue].append(color_light_dark)
        # red
        self.colors[Color.red] = "#FF0000"
        color_light_dark = ["#FF9090", "#B30006"]
        self.colors_gradient_lookup[Color.red] = list()
        self.colors_gradient_lookup[Color.red].append(color_light_dark)
        # green
        self.colors[Color.green] = "#08A105"
        color_light_dark = ["#90FF9B", "#00B306"]
        self.colors_gradient_lookup[Color.green] = list()
        self.colors_gradient_lookup[Color.green].append(color_light_dark)
        # yellow
        self.colors[Color.yellow] = "#FCFF00"
        color_light_dark = ["#FFFC90", "#B0B300"]
        self.colors_gradient_lookup[Color.yellow] = list()
        self.colors_gradient_lookup[Color.yellow].append(color_light_dark)
        # pink
        self.colors[Color.pink] = "#FF00D5"
        color_light_dark = ["#FF90E6", "#B300A4"]
        self.colors_gradient_lookup[Color.pink] = list()
        self.colors_gradient_lookup[Color.pink].append(color_light_dark)
        # purple
        self.colors[Color.purple] = "#8D00FF"
        color_light_dark = ["#D190FF", "#8600B3"]
        self.colors_gradient_lookup[Color.purple] = list()
        self.colors_gradient_lookup[Color.purple].append(color_light_dark)
        # orange
        self.colors[Color.orange] = "#FFD500"
        color_light_dark = ["#FFEA7C", "#E7C101"]
        self.colors_gradient_lookup[Color.orange] = list()
        self.colors_gradient_lookup[Color.orange].append(color_light_dark)
        # grey
        self.colors[Color.grey] = "#737171"
        color_light_dark = ["#DBD9D9", "#6B6B6B"]
        self.colors_gradient_lookup[Color.grey] = list()
        self.colors_gradient_lookup[Color.grey].append(color_light_dark)
        # dark_grey
        self.colors[Color.dark_grey] = "#575656"
        color_light_dark = ["#AAA8A8", "#353535"]
        self.colors_gradient_lookup[Color.dark_grey] = list()
        self.colors_gradient_lookup[Color.dark_grey].append(color_light_dark)

    def __word_wrap(self, text, max_length):
        dedented_text = textwrap.dedent(text).strip()
        wrapped_text = textwrap.fill(dedented_text, width=max_length)
        rows = len(wrapped_text.split("\n"))
        return wrapped_text, rows

    def __generate_row_labels_html(self):
        (wrapped_text, rows_count) = self.__word_wrap(self.__label, 25)
        letter_size = int(self.__scaling * (1 / 7))
        center_offset_y = ((self.__pos_y * self.__scaling) + self.__scaling / 2) + self.__offset_y - (((rows_count - 1) * letter_size) / 2)
        start_label_x = offset_x - int(self.__scaling * (1 / 7))
        frame_html = ""
        frame_html += "context.fillStyle = '" + str(self.colors_gradient_lookup[Color.dark_grey][0][1]) + "';\n"
        frame_html += "context.textAlign = 'right';\n"
        frame_html += "context.font = 'normal " + str(letter_size) + "pt Calibri';\n"
        tmp_arr = wrapped_text.split("\n")
        for text_i in range(0, len(tmp_arr)):
            frame_html += "context.fillText('" + str(tmp_arr[text_i]) + "', " + str(start_label_x) + "," + str(center_offset_y + text_i * (letter_size + 3)) + ");\n"
        return frame_html

    def __generate_col_labels_html(self):
        # execute self.__word_wrap()
        (wrapped_text, rows_count) = self.__word_wrap(self.__label, 25)
        start_label_x = 0
        center_offset_y = self.__offset_y
        letter_size = int(self.__scaling * (1 / 7))
        tr_x = self.__offset_x + self.__pos_x * self.__scaling + (self.__scaling / 4) - (((rows_count - 1) * letter_size) / 2)
        tr_y = self.__offset_y - (self.__offset_y / 7)
        frame_html = ""
        frame_html += "context.save();\n"
        frame_html += "context.translate(" + str(tr_x) + "," + str(tr_y) + ");\n"
        frame_html += "context.rotate(-Math.PI / 4 );\n"
        frame_html += "context.fillStyle = '" + str(self.colors_gradient_lookup[Color.dark_grey][0][1]) + "';\n"
        frame_html += "context.textAlign = 'left';\n"
        frame_html += "context.font = 'bold " + str(letter_size) + "pt Calibri';\n"
        tmp_arr = wrapped_text.split("\n")
        for text_i in range(0, len(tmp_arr)):
            frame_html += "context.fillText('" + str(tmp_arr[text_i]) + "', " + \
                                                 str(start_label_x + text_i * (letter_size + 1)) + "," + \
                                                 str(center_offset_y / 8 + text_i * (letter_size + 3)) + ");\n"
        frame_html += "context.restore();\n"
        return frame_html

    def __generate_html_code(self):
        if self.__row_or_col == RowCol.row:
            label_html = self.__generate_row_labels_html()
        else:
            label_html = self.__generate_col_labels_html()
        return label_html

    def __str__(self):
        return self.__generate_html_code()

# DESCRIPTION: Computes Box-Whisker Plots for a given input
# INPUT:
#   - legend_names <string> : corresponds to sub-column names
#   - column_count <int> : to compute the position for the legend
#   - factor <float> : Whisker-Plots are between grid and legend and the Whisker-Plots can independently scaled.
#                      Factor correlates with the Whisker-Plot scaling.
#   - scaling=73 <float> : global scaling
#   - offset_x=0 <float> : global offset for canvas_x
#   - offset_y=0 <float> : global offset for canvas_y
# OUTPUT: str(<Legend>) => HTML-Code
class Legend:
    def __init__(self, legend_names, column_count, factor=1 ,scaling=73, offset_x=0, offset_y=0):
        self.__legend_names = legend_names
        self.__column_count = column_count
        self.__scaling = scaling
        self.__factor = factor
        self.__offset_x = offset_x
        self.__offset_y = offset_y
        self.__colors()

    def __colors(self):
        # [blue,red,green,yellow,pink,purple]
        self.colors = dict()
        self.colors_gradient_lookup = dict()
        # blue
        self.colors[Color.blue] = "#0044FF"
        color_light_dark = ["#8ED6FF", "#004CB3"]
        self.colors_gradient_lookup[Color.blue] = list()
        self.colors_gradient_lookup[Color.blue].append(color_light_dark)
        # red
        self.colors[Color.red] = "#FF0000"
        color_light_dark = ["#FF9090", "#B30006"]
        self.colors_gradient_lookup[Color.red] = list()
        self.colors_gradient_lookup[Color.red].append(color_light_dark)
        # green
        self.colors[Color.green] = "#08A105"
        color_light_dark = ["#90FF9B", "#00B306"]
        self.colors_gradient_lookup[Color.green] = list()
        self.colors_gradient_lookup[Color.green].append(color_light_dark)
        # yellow
        self.colors[Color.yellow] = "#FCFF00"
        color_light_dark = ["#FFFC90", "#B0B300"]
        self.colors_gradient_lookup[Color.yellow] = list()
        self.colors_gradient_lookup[Color.yellow].append(color_light_dark)
        # pink
        self.colors[Color.pink] = "#FF00D5"
        color_light_dark = ["#FF90E6", "#B300A4"]
        self.colors_gradient_lookup[Color.pink] = list()
        self.colors_gradient_lookup[Color.pink].append(color_light_dark)
        # purple
        self.colors[Color.purple] = "#8D00FF"
        color_light_dark = ["#D190FF", "#8600B3"]
        self.colors_gradient_lookup[Color.purple] = list()
        self.colors_gradient_lookup[Color.purple].append(color_light_dark)
        # orange
        self.colors[Color.orange] = "#FFD500"
        color_light_dark = ["#FFEA7C", "#E7C101"]
        self.colors_gradient_lookup[Color.orange] = list()
        self.colors_gradient_lookup[Color.orange].append(color_light_dark)
        # grey
        self.colors[Color.grey] = "#737171"
        color_light_dark = ["#DBD9D9", "#6B6B6B"]
        self.colors_gradient_lookup[Color.grey] = list()
        self.colors_gradient_lookup[Color.grey].append(color_light_dark)
        # dark_grey
        self.colors[Color.dark_grey] = "#575656"
        color_light_dark = ["#AAA8A8", "#353535"]
        self.colors_gradient_lookup[Color.dark_grey] = list()
        self.colors_gradient_lookup[Color.dark_grey].append(color_light_dark)

    def __generate_html_code(self):
        start_x = (self.__scaling * self.__column_count) + self.__offset_x + (1.5*self.__scaling) + \
                  (self.__scaling * self.__factor)
        start_y = self.__offset_y
        letter_size = int(self.__scaling * (1 / 8))
        bar_size = self.__scaling / 6
        frame_html = ""
        for i in range(0, len(self.__legend_names)):
            # square 1
            frame_html += "context.beginPath();\n"
            frame_html += "context.moveTo(" + str(start_x) + "," + str(start_y + (i * bar_size) * 1.5 ) + ");\n"
            frame_html += "context.lineTo(" + str(start_x + bar_size) + "," + str(start_y + (i * bar_size) * 1.5) + ");\n"
            frame_html += "context.lineWidth = " + str(bar_size) + ";\n"
            frame_html += "context.strokeStyle = '" + str(self.colors_gradient_lookup[Color(i)][0][0]) + "';\n"
            frame_html += "context.stroke();\n"
            # square 1
            frame_html += "context.beginPath();\n"
            frame_html += "context.moveTo(" + str(start_x + bar_size) + "," + str(start_y + (i * bar_size) * 1.5 ) + ");\n"
            frame_html += "context.lineTo(" + str(start_x + (2 * bar_size)) + "," + str(start_y + (i * bar_size) * 1.5) + ");\n"
            frame_html += "context.lineWidth = " + str(bar_size) + ";\n"
            frame_html += "context.strokeStyle = '" + str(self.colors_gradient_lookup[Color(i)][0][1]) + "';\n"
            frame_html += "context.stroke();\n"
            # labels
            frame_html += "context.fillStyle = '" + str(self.colors_gradient_lookup[Color.dark_grey][0][1]) + "';\n"
            frame_html += "context.textAlign = 'left';\n"
            frame_html += "context.font = 'italic " + str(letter_size) + "pt Calibri';\n"
            label_x = start_x + (2.4 * bar_size)
            label_y = start_y + ((i * bar_size) * 1.5 ) + (bar_size / 4.5)
            frame_html += "context.fillText('" + str(self.__legend_names[i]) + "', " + str(label_x) + "," + str(label_y) + ");\n"
        return frame_html

    def __str__(self):
        return self.__generate_html_code()


# DESCRIPTION: Computes Box-Whisker Plots for a given input
# INPUT:
#   - row_y <int> : row to print
#   - row_data <<list>row_data[Color(i)]> : returns array with row values for each color
#   - max_value <float> : |max_Value| is needed for scaling
#   - max_cols <int> : max number of columns is needed to compute the right position
#   - num_values <float> : #{sub_column_names}
#   - width_factor <float> : special scaling for Box-Whisker plot
#   - log_type <string>[log2, log10, ln, na] : default is log2 from the main function
#   - scale_on_off <string>[on, off] : compute scale on or off (HTML)
#   - scaling=73 <float> : global scaling
#   - offset_x=0 <float> : global offset for canvas_x
#   - offset_y=0 <float> : global offset for canvas_y
# OUTPUT: str(<BoxWhisker>) => HTML-Code
class BoxWhisker:
    def __init__(self, row_y, row_data, max_value, max_cols, num_values, width_factor, log_type, scale_on_off, scaling=73, offset_x=0, offset_y=0):
        self.__row_y = row_y
        self.__row_data = row_data
        self.__max_value = max_value
        self.__max_cols = max_cols
        self.__num_values = num_values
        self.__width_factors = width_factor
        self.__scaling = scaling
        self.__log_type = log_type
        self.__scale_on_off =  scale_on_off
        self.__offset_x = offset_x
        self.__offset_y = offset_y
        self.__colors()
        self.__compute_diameter()

    def __inverse_log2(self, value):
        return pow(2, value)
    def __inverse_log10(self, value):
        return pow(10, value)
    def __inverse_ln(self, value):
        return exp(value)
    def __inverse_non_log(self, value):
        return (value)
    def __log2(self, value):
        return log2(value)
    def __log10(self, value):
        return log10(value)
    def __ln(self, value):
        return log(value)
    def __non_log(self, value):
        return (value)

    def __colors(self):
        # [blue,red,green,yellow,pink,purple]
        self.colors = dict()
        self.colors_gradient_lookup = dict()
        # blue
        self.colors[Color.blue] = "#0044FF"
        color_light_dark = ["#8ED6FF", "#004CB3"]
        self.colors_gradient_lookup[Color.blue] = list()
        self.colors_gradient_lookup[Color.blue].append(color_light_dark)
        # red
        self.colors[Color.red] = "#FF0000"
        color_light_dark = ["#FF9090", "#B30006"]
        self.colors_gradient_lookup[Color.red] = list()
        self.colors_gradient_lookup[Color.red].append(color_light_dark)
        # green
        self.colors[Color.green] = "#08A105"
        color_light_dark = ["#90FF9B", "#00B306"]
        self.colors_gradient_lookup[Color.green] = list()
        self.colors_gradient_lookup[Color.green].append(color_light_dark)
        # yellow
        self.colors[Color.yellow] = "#FCFF00"
        color_light_dark = ["#FFFC90", "#B0B300"]
        self.colors_gradient_lookup[Color.yellow] = list()
        self.colors_gradient_lookup[Color.yellow].append(color_light_dark)
        # pink
        self.colors[Color.pink] = "#FF00D5"
        color_light_dark = ["#FF90E6", "#B300A4"]
        self.colors_gradient_lookup[Color.pink] = list()
        self.colors_gradient_lookup[Color.pink].append(color_light_dark)
        # purple
        self.colors[Color.purple] = "#8D00FF"
        color_light_dark = ["#D190FF", "#8600B3"]
        self.colors_gradient_lookup[Color.purple] = list()
        self.colors_gradient_lookup[Color.purple].append(color_light_dark)
        # orange
        self.colors[Color.orange] = "#FFD500"
        color_light_dark = ["#FFEA7C", "#E7C101"]
        self.colors_gradient_lookup[Color.orange] = list()
        self.colors_gradient_lookup[Color.orange].append(color_light_dark)
        # grey
        self.colors[Color.grey] = "#737171"
        color_light_dark = ["#DBD9D9", "#6B6B6B"]
        self.colors_gradient_lookup[Color.grey] = list()
        self.colors_gradient_lookup[Color.grey].append(color_light_dark)
        # dark_grey
        self.colors[Color.dark_grey] = "#575656"
        color_light_dark = ["#AAA8A8", "#353535"]
        self.colors_gradient_lookup[Color.dark_grey] = list()
        self.colors_gradient_lookup[Color.dark_grey].append(color_light_dark)
        # background
        self.colors[Color.dark_grey] = "#575656"
        color_light_bkg = ["#FAFAFA", "#F2F2F2"]
        self.colors_gradient_lookup["bkg"] = list()
        self.colors_gradient_lookup["bkg"].append(color_light_bkg)

    def __compute_diameter(self):
        self.__line_color = self.colors[Color.dark_grey]
        self.__line_width = 1
        self.__start_x = self.__offset_x + (self.__max_cols * self.__scaling) + 80
        self.__end_x = self.__start_x + (self.__scaling * self.__width_factors)
        self.__start_y = self.__offset_y + (row_y * self.__scaling)
        self.__data_shift_y = self.__scaling / self.__num_values - 2
        self.__center_zero_x = (self.__end_x - self.__start_x) / 2 + self.__start_x
        self.__new_scaling = self.__scaling * self.__width_factors

    def __compute_ticks(self, x1, y1, x2, y2):
        center_x = x1 + ((x2 - x1) / 2)
        center_y = y1
        tick_length = 2
        num_of_ticks = 3
        new_max_val = self.__max_value
        value_step = self.__max_value / num_of_ticks
        tick_range = (((x2 - x1) / 2) / num_of_ticks)
        self.__tick_list = list()
        for i in range(1, num_of_ticks):
            tick_value = (value_step * i)
            # plus range -y
            tick_x_start = center_x - (tick_range * i)
            tick_y_start = center_y
            tick_x_end = center_x - (tick_range * i)
            tick_y_end = center_y - tick_length
            self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round(((-1) * tick_value), 1)])
            # minus range +y
            tick_x_start = center_x + (tick_range * i)
            tick_x_end = center_x + (tick_range * i)
            self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round((tick_value), 1)])
        # add center tick
        tick_x_start = center_x
        tick_y_start = center_y
        tick_x_end = center_x
        tick_y_end = center_y - tick_length - 3
        self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, 0])
        # add end ticks
        tick_x_start = x1
        tick_y_start = y1
        tick_x_end = x1
        tick_y_end = y1 - tick_length - 3
        self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round(((-1) * new_max_val), 1)])
        tick_x_start = x2
        tick_y_start = y2
        tick_x_end = x2
        tick_y_end = y2 - tick_length - 3
        self.__tick_list.append([tick_x_start, tick_y_start, tick_x_end, tick_y_end, round(new_max_val, 1)])
        frame_html = ""
        for sub_arr in self.__tick_list:
            frame_html += "context.beginPath();\n"
            frame_html += "context.moveTo(" + str(sub_arr[0]) + "," + str(sub_arr[1]) + ");\n"
            frame_html += "context.lineTo(" + str(sub_arr[2]) + "," + str(sub_arr[3]) + ");\n"
            frame_html += "context.lineWidth = " + str(self.__line_width) + ";\n"
            frame_html += "context.strokeStyle = '" + str(self.__line_color) + "';\n"
            frame_html += "context.stroke();\n"
        count = 0
        max_count_center = len(self.__tick_list) - 3
        max_count_start_tick = len(self.__tick_list) - 2
        max_count_end_tick = len(self.__tick_list) - 1
        letter_size = float(self.__scaling * (1 / 11)) + (self.__width_factors)
        letter_size_2 = float(self.__scaling * (1 / 18)) + (self.__width_factors * (1.5))
        scaling_left = int(self.__new_scaling) * (1 / 65) #(180 -> 12)
        scaling_normal = int(self.__new_scaling * (1 / 60)) #(180 -> 6)
        scaling_right = int(self.__new_scaling * (1 / 65)) #(180 -> 3)
        for sub_arr in self.__tick_list:
            frame_html += "context.fillStyle = '" + str(self.colors_gradient_lookup[Color.dark_grey][0][1]) + "';\n"
            frame_html += "context.textAlign = 'center';\n"
            if count == max_count_start_tick:
                frame_html += "context.font = 'bold " + str(letter_size) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0] - scaling_left) + "," + str((sub_arr[3] - 7)) + ");\n"
            elif count == max_count_end_tick:
                frame_html += "context.font = 'bold " + str(letter_size) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0] + scaling_right) + "," + str((sub_arr[3] - 7)) + ");\n"
            elif count == max_count_center:
                frame_html += "context.font = 'bold " + str(letter_size) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0]) + "," + str((sub_arr[3] - scaling_normal)) + ");\n"
            else:
                frame_html += "context.font = 'italic " + str(letter_size_2) + "pt Calibri';\n"
                frame_html += "context.fillText('" + str(sub_arr[4]) + "'," + str(sub_arr[0]) + "," + str((sub_arr[3] - scaling_normal)) + ");\n"
            count += 1
        return frame_html

    def __draw_scaling_axis(self):
        color = self.colors[Color.dark_grey]
        line_width = 1
        x1 = self.__start_x
        y1 = self.__start_y
        x2 = self.__start_x + (self.__scaling * self.__width_factors)
        y2 = self.__start_y
        frame_html = "context.beginPath();\n"
        frame_html += "context.moveTo(" + str(x1) + "," + str(y1) + ");\n"
        frame_html += "context.lineTo(" + str(x2) + "," + str(y2) + ");\n"
        frame_html += "context.lineWidth = " + str(line_width) + ";\n"
        frame_html += "context.strokeStyle = '" + str(color) + "';\n"
        frame_html += "context.stroke();\n"
        # ticks + numbers
        frame_html += self.__compute_ticks(x1, y1, x2, y2)
        return frame_html

    def __compute_box_whisker_values(self, row_data, color):
        inv_log_func_dict = {'log2' : self.__inverse_log2, 'log10' : self.__inverse_log10, 'ln' : self.__inverse_ln, 'na' : self.__inverse_non_log}
        log_func_dict = {'log2' : self.__log2, 'log10' : self.__log10, 'ln' : self.__ln, 'na' : self.__non_log}
        box_whisker_element = {"median" : 0.0, "upper_quartile" : 0.0 , "lower_quartile" : 0.0,
                               "upper_whisker" : 0, "lower_whisker" : 0.0}

        box_whisker_element_coord = {"median_x" : 0.0, "median_y" : 0.0,
                                     "upper_quartile_x" : 0.0 , "upper_quartile_y" : 0.0,
                                     "lower_quartile_x" : 0.0 , "lower_quartile_y" : 0.0,
                                     "upper_whisker_x" : 0.0 , "upper_whisker_y" : 0.0,
                                     "lower_whisker_x" : 0.0 , "lower_whisker_y" : 0.0}
        # transfer log to non-log data
        for i in range(0, len(row_data)):
            row_data[i] = inv_log_func_dict[self.__log_type](row_data[i])
        # list to numpy array
        data = np.asanyarray(row_data, dtype=np.float32)
        # compute specific values for Box-Whiskers
        B = plt.boxplot(data)
        foo = [item.get_ydata() for item in B['whiskers']]
        # compute specific values for Box-Whiskers
        box_whisker_element["median"] = log_func_dict[self.__log_type](np.median(data))
        box_whisker_element["upper_quartile"] = log_func_dict[self.__log_type](foo[1][0])
        box_whisker_element["lower_quartile"] = log_func_dict[self.__log_type](foo[0][0])
        box_whisker_element["upper_whisker"] = log_func_dict[self.__log_type](foo[1][1])
        box_whisker_element["lower_whisker"] = log_func_dict[self.__log_type](foo[0][1])
        # transfer values to coordinates (x-values)
        new_max_val = self.__max_value
        max_x_range = (self.__end_x - self.__center_zero_x)
        box_whisker_element_coord["median_x"] = self.__center_zero_x + (box_whisker_element["median"] * max_x_range / new_max_val)
        box_whisker_element_coord["upper_quartile_x"] = self.__center_zero_x + (box_whisker_element["upper_quartile"] * max_x_range / new_max_val)
        box_whisker_element_coord["lower_quartile_x"] = self.__center_zero_x + (box_whisker_element["lower_quartile"] * max_x_range / new_max_val)
        box_whisker_element_coord["upper_whisker_x"] = self.__center_zero_x + (box_whisker_element["upper_whisker"] * max_x_range / new_max_val)
        box_whisker_element_coord["lower_whisker_x"] = self.__center_zero_x + (box_whisker_element["lower_whisker"] * max_x_range / new_max_val)
        return box_whisker_element_coord

    def __draw_median(self, median, plot_i, tmp_offset_y):
        x1 = round(median,0)
        y1 = round(self.__start_y + (plot_i * tmp_offset_y) + 1, 0)
        x2 = round(median, 0)
        y2 = round(self.__start_y + (plot_i * tmp_offset_y) - 1 + (tmp_offset_y), 0)
        str_w = 1.5
        median_html = "context.beginPath();\n"
        median_html += "context.moveTo(" + str(x1) + "," + str(y1) + ");\n"
        median_html += "context.lineTo(" + str(x2) + "," + str(y2) + ");\n"
        median_html += "context.lineWidth = " + str(str_w) + ";\n"
        median_html += "context.strokeStyle = '#000000';\n"
        median_html += "context.stroke();\n"
        return median_html

    def __draw_upper_lower_quartile(self, upper_quartile_x, lower_quartile_x, plot_i, tmp_offset_y, color):
        diff_x = upper_quartile_x - lower_quartile_x
        y1 = round(self.__start_y + (plot_i * tmp_offset_y) + 1, 0)
        y2 = round(self.__start_y + (plot_i * tmp_offset_y) - 1 + (tmp_offset_y), 0)
        y2_diff = y2 - y1
        ul_quartile_html = "context.beginPath();\n"
        ul_quartile_html += "context.rect(" + str(lower_quartile_x) + "," + str(y1) + "," + \
                                              str(diff_x) + "," + str(y2_diff) + ");\n"
        #ul_quartile_html += "context.fillStyle = '" + str(self.colors_gradient_lookup[color][0][0]) + "';\n"
        ul_quartile_html += "context.fillStyle = '" + str(self.colors[color]) + "';\n"

        ul_quartile_html += "context.fill();\n"
        ul_quartile_html += "context.lineWidth = 1;\n"
        #ul_quartile_html += "context.strokeStyle = '" + str(self.colors_gradient_lookup[color][0][1]) + "';\n"
        ul_quartile_html += "context.strokeStyle = '" + str(self.colors_gradient_lookup[color][0][1]) + "';\n"

        ul_quartile_html += "context.stroke();\n"
        return ul_quartile_html

    def __draw_upper_lower_whisker(self, upper_whisker_x, lower_whisker_x, plot_i, tmp_offset_y, color):
        x1 = round(lower_whisker_x, 1)
        y1 = round(self.__start_y + (plot_i * tmp_offset_y) + (tmp_offset_y/2), 1)
        x2 = round(upper_whisker_x, 1)
        y2 = round(self.__start_y + (plot_i * tmp_offset_y) + (tmp_offset_y/2), 1)
        dash_shift = tmp_offset_y / 4
        str_w = 1
        ul_whisker_html = "context.beginPath();\n"
        ul_whisker_html += "context.moveTo(" + str(x1) + "," + str(y1) + ");\n"
        ul_whisker_html += "context.lineTo(" + str(x2) + "," + str(y2) + ");\n"
        ul_whisker_html += "context.lineWidth = " + str(str_w) + ";\n"
        ul_whisker_html += "context.strokeStyle = '" + str(self.colors_gradient_lookup[color][0][1]) + "';\n"
        ul_whisker_html += "context.stroke();\n"
        # lower whisker dash
        ul_whisker_html += "context.beginPath();\n"
        ul_whisker_html += "context.moveTo(" + str(x1) + "," + str(y1 - dash_shift) + ");\n"
        ul_whisker_html += "context.lineTo(" + str(x1) + "," + str(y1 + dash_shift) + ");\n"
        ul_whisker_html += "context.lineWidth = " + str(str_w) + ";\n"
        ul_whisker_html += "context.strokeStyle = '" + str(self.colors_gradient_lookup[color][0][1]) + "';\n"
        ul_whisker_html += "context.stroke();\n"
        # upper whisker dash
        ul_whisker_html += "context.beginPath();\n"
        ul_whisker_html += "context.moveTo(" + str(x2) + "," + str(y2 - dash_shift) + ");\n"
        ul_whisker_html += "context.lineTo(" + str(x2) + "," + str(y2 + dash_shift) + ");\n"
        ul_whisker_html += "context.lineWidth = " + str(str_w) + ";\n"
        ul_whisker_html += "context.strokeStyle = '" + str(self.colors_gradient_lookup[color][0][1]) + "';\n"
        ul_whisker_html += "context.stroke();\n"
        return ul_whisker_html

    def __draw_background(self):
        frame_html = ""
        if (row_y%2) == 0:
            color = self.colors_gradient_lookup["bkg"][0][0]
        else:
            color = self.colors_gradient_lookup["bkg"][0][1]
        x1 = self.__start_x
        y1 = self.__start_y
        x1_shift = self.__scaling * self.__width_factors
        y1_shift = self.__scaling + self.__scaling * self.__row_y
        frame_html = "context.beginPath();\n"
        frame_html += "context.rect(" + str(x1) + "," + str(y1) + "," + \
                                              str(x1_shift) + "," + str(y1_shift) + ");\n"
        frame_html += "context.fillStyle = '" + str(color) + "';\n"
        frame_html += "context.fill();\n"
        frame_html += "context.lineWidth = 1;\n"
        frame_html += "context.strokeStyle = '" + str(color) + "';\n"
        frame_html += "context.stroke();\n"
        return frame_html

    def __generate_html_code(self):
        frame_html = ""
        frame_html += self.__draw_background()
        if self.__scale_on_off == "on":
            frame_html += self.__draw_scaling_axis()

        for i in range(0, len(row_data)):
            box_whisker_element_coord = self.__compute_box_whisker_values(row_data[Color(i)], Color(i))
            frame_html += self.__draw_upper_lower_whisker(box_whisker_element_coord["upper_whisker_x"],
                                                          box_whisker_element_coord["lower_whisker_x"],
                                                          i, self.__data_shift_y, Color(i))
            frame_html += self.__draw_upper_lower_quartile(box_whisker_element_coord["upper_quartile_x"],
                                                           box_whisker_element_coord["lower_quartile_x"],
                                                           i, self.__data_shift_y, Color(i))
            frame_html += self.__draw_median(box_whisker_element_coord["median_x"], i, self.__data_shift_y)
        return frame_html

    def __str__(self):
        return self.__generate_html_code()


def prepare_data_for_BoxWhisker(input_for_element_class, num_columns):
    prepared_output = list()
    row_result = dict()
    count_rows = 0
    start = "false"
    for sub in input_for_element_class:
        if start == "false":
            row_result = dict()
            count_rows = 0
            start = "true"
        if count_rows < (num_columns - 1) and start == "true":
            for key in sub[3]:
                if key in row_result:
                    row_result[key].append(sub[3][key])
                else:
                    row_result[key] = list()
                    row_result[key].append(sub[3][key])
        elif start == "true":
            # last column
            for key in sub[3]:
                if key in row_result:
                    row_result[key].append(sub[3][key])
                else:
                    row_result[key] = list()
                    row_result[key].append(sub[3][key])
            prepared_output.append(row_result)
            start = "false"
        count_rows += 1
    return prepared_output

def create_element_class_input(act_x, act_y, max_value, sub_package, y_box_size, offset_x, offset_y):
    #log_scaled_dict = {Color.blue : 8, Color.red : 0, Color.green : 10, Color.pink : 4}
    # Element(x, y, max_log_value, log_scaled_dict, args.scale, offset_x, offset_y)
    tmp_hash = dict()
    for i in range(0, len(sub_package)):
        if float(sub_package[i]) == 0:
            tmp_hash[Color(i)] = 0
        else:
            tmp_hash[Color(i)] = float(sub_package[i])
    element_package = list()
    element_package.append(act_x)
    element_package.append(act_y)
    element_package.append(max_value)
    element_package.append(tmp_hash)
    element_package.append(y_box_size)
    element_package.append(offset_x)
    element_package.append(offset_y)
    return element_package

def parse_input(input_table, y_box_size, in_offset_x, in_offset_y):
    input_for_element_class = list()
    sub_packages_list = list()
    sub_column_names = list()
    column_names = list()
    row_names = list()
    counter_x = 0
    counter_y = 0
    max_value = 0
    h_size = 0
    w_size = 0
    title = ""
    with open(input_table, "r") as fh:
        for line in fh:
            line = line.rstrip()
            tmp_line_arr = line.split("\t")
            if tmp_line_arr[0] == "#title:":
                title = tmp_line_arr[1]
            if tmp_line_arr[0] == "#col_names:":
                counter_x = int(len(tmp_line_arr) - 1)
                #w_size = int((len(tmp_line_arr) - 1) * y_box_size + in_offset_x + 300)
                for i in range(1,len(tmp_line_arr)):
                    column_names.append(tmp_line_arr[i])
            elif tmp_line_arr[0] == "#sub_col:":
                for i in range(1,len(tmp_line_arr)):
                    sub_column_names.append(tmp_line_arr[i])
            if tmp_line_arr[0] != "#col_names:" and tmp_line_arr[0] != "#sub_col:" and tmp_line_arr[0] != "#title:":
                row_names.append(tmp_line_arr[0])
                for i in range(1, len(tmp_line_arr)):
                    int_arr = tmp_line_arr[i].split(",")
                    int_arr = [float(s) for s in int_arr]
                    tmp_int_arr = [fabs(s) for s in int_arr]
                    sub_values = sorted(tmp_int_arr, reverse=True)[0]
                    if float(sub_values) > fabs(max_value):
                        max_value = fabs(sub_values)
                    sub_package = list()
                    for j in range(0, len(int_arr)):
                        sub_package.append(int_arr[j])
                    sub_packages_list.append(sub_package)
            counter_y += 1
    w_size = int(len(column_names) * y_box_size + in_offset_x + 1500)
    h_size = int(len(row_names) * y_box_size + in_offset_y + 10)
    # setup input_for_element_class
    act_x = -1
    act_y = 0
    for sub_package in sub_packages_list:
        act_x += 1
        if act_x < counter_x:
            tmp_class_input = create_element_class_input(act_x, act_y, max_value, sub_package, y_box_size, offset_x, offset_y)
        else:
            act_x = 0
            act_y += 1
            tmp_class_input = create_element_class_input(act_x, act_y, max_value, sub_package, y_box_size, offset_x, offset_y)
        input_for_element_class.append(tmp_class_input)
    return column_names, row_names, sub_column_names, input_for_element_class, int(w_size), int(h_size), max_value, title

def validate_input_file(file_to_check):
    lookup = {"#col_names:" : 0, "#sub_col:" : 0, "#title:" : 0}
    message = ""
    fh = open(file_to_check, "r")
    counter = 1
    key_counter = 0
    for line in fh:
        line = line.rstrip()
        arr_line = line.split("\t")
        if arr_line[0] in lookup:
            lookup[arr_line[0]] = (len(arr_line) - 1)
            key_counter += 1
        else:
            if key_counter != len(lookup):
                message = "To less/many hashtag lines (#...), see line: " + str(counter)
                return -1, message
            # check num of cols
            if (len(arr_line) - 1) != lookup["#col_names:"]:
                message = "To less/many columns in line: " + str(counter)
                return -1, message
            # check num of sub columns
            for sub_i in range(1,len(arr_line)):
                sub_i_length = len(arr_line[sub_i].split(","))
                if sub_i_length != lookup["#sub_col:"]:
                    message = "To less/many numbers in column, see line: " + str(counter)
                    return -1, message
        counter += 1
    fh.close()
    return 0, message

def generate_html_title(title, scale, offset_x,):
    x_pos = offset_x + (scale / 2)
    y_pos = (scale / 1.5)
    size = scale / 3.2
    output_html = ""
    output_html += "context.font = 'bold " + str(size) + "pt Calibri';\n"
    output_html += "context.fillText('" + str(title) + "', " + str(x_pos) + "," + str(y_pos) + ");\n"
    return output_html

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_table", help="merged table from MEGAN", type=str, required=True)
    parser.add_argument("-o", "--out_file", help="output.html (default: STDOUT)", type=str, default="STDOUT")
    parser.add_argument("-s", "--scale", help="x-length of each box (default: 100)", type=int, default=100)
    parser.add_argument("-l", "--log_type", help="log-type: 'na' , 'log2' , 'log10' , 'ln' (default: log2)", type=str, default="log2")
    parser.add_argument("-w", "--whisker_scale", help="Spread Box-Whisker-Plot (default: 2)", type=float, default=2)
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    # validate commandline parameters
    log_mode = {"na" : 0, "log2" : 0, "log10" : 0, "ln" :0}
    if args.log_type not in log_mode:
        print(str(args.log_type) + " is not available!")
        exit()
    # validate input-file
    (status, message) = validate_input_file(args.in_table)
    if status == -1:
        print(message)
        exit()

    # global offset => dynamical scaling
    offset_x = 23 * (args.scale / 8)
    offset_y = 23 * (args.scale / 8)

    # parse input file (list(),list(),list(),int(val)) and create Elements (Class)
    (column_names, row_names, sub_column_names, input_for_element_class, w_size, h_size, max_value, title) = \
        parse_input(args.in_table, args.scale, offset_x, offset_y)

    # prepare data for BoxWhisker Class
    prepared_output = prepare_data_for_BoxWhisker(input_for_element_class, len(column_names))

    # template start
    output_html = "<!DOCTYPE HTML>\n" + "<html>\n" + " <head>\n" + "<title>" + str(title) + "</title>\n" + "  <style>\n"
    output_html += "   body {\n" + "    margin: 0px;\n" + "    padding: 0px;\n"
    output_html += "   }\n" + "  </style>\n" + " </head>\n" + " <body>\n"
    output_html += "  <canvas id=\"myCanvas\" width=\"" + str(w_size) + "\" height=\"" + str(h_size) + "\"></canvas>\n"
    output_html += "  <script>\n"
    # START script sources
    output_html += "   var canvas = document.getElementById('myCanvas');\n"
    output_html += "   var context = canvas.getContext('2d');\n"
    # write column/row names
    # (TITLE)
    new_element = generate_html_title(title, args.scale, offset_x)
    output_html += str(new_element)
    # (A) iterate through data set (Element class)
    for sub in input_for_element_class:
        new_element = Element(sub[0], sub[1], sub[2], sub[3], sub[4], sub[5], sub[6])
        output_html += str(new_element)
    # (B) add row labels
    for row_i in range(0, len(row_names)):
        new_name = Label(RowCol.row, 0, row_i, row_names[row_i], args.scale, offset_x, offset_y)
        output_html += str(new_name)
    # (C) add column labels
    for col_i in range(0, len(column_names)):
        new_name = Label(RowCol.col, col_i, 0, column_names[col_i], args.scale, offset_x, offset_y)
        output_html += str(new_name)
    # (D) box whisker plot
    row_y = 0
    for row_data in prepared_output:
        if row_y == 0:
            new_box_whisker = BoxWhisker(row_y, row_data, max_value, len(column_names), len(sub_column_names),
                                         args.whisker_scale, args.log_type, "on" ,args.scale, offset_x, offset_y)
        else:
            new_box_whisker = BoxWhisker(row_y, row_data, max_value, len(column_names), len(sub_column_names),
                                         args.whisker_scale, args.log_type, "off" ,args.scale, offset_x, offset_y)
        output_html += str(new_box_whisker)
        row_y += 1
    # (E) add color legend
    new_legend = Legend(sub_column_names, len(column_names), args.whisker_scale , args.scale, offset_x, offset_y)
    output_html += str(new_legend)
    # (F) add scaling
    for row_num in range(0, len(row_names)):
        new_scale = Scale(len(column_names), row_num, max_value, args.scale, offset_x, offset_y)
        output_html += str(new_scale)

    # STOP script sources
    # template stop
    output_html += "  </script>\n"
    output_html += " </body>\n"
    output_html += "</html>\n"

    # write output to file or stdout
    if args.out_file == "STDOUT":
        print()
        print(str(output_html))
    else:
        fh = open(args.out_file, "w")
        fh.write(str(output_html) + "\n")