import json
import pyautogui
import tkinter
from PIL import Image, ImageDraw, ImageGrab, ImageTk
import cv2
import numpy
import keyboard
import os

dirname = os.path.dirname(__file__)

config = json.load(open("config.json"))

screen_width = config["screen_bbox"][2] - config["screen_bbox"][0]
screen_height = config["screen_bbox"][3] - config["screen_bbox"][1]

top_left_point = (220/700 * screen_width + config["screen_bbox"][0], 106/600 * screen_height + config["screen_bbox"][1])
top_left_point_diagonal = (246/700 * screen_width + config["screen_bbox"][0], 91/600 * screen_height + config["screen_bbox"][1])
top_left_point_vertical = (220/700 * screen_width + config["screen_bbox"][0], 138/600 * screen_height + config["screen_bbox"][1])
top_right_point = (486/700 * screen_width + config["screen_bbox"][0], 126/600 * screen_height + config["screen_bbox"][1])

pixel_width = (top_right_point[0] - top_left_point[0]) / 5
pixel_height = (top_left_point_vertical[1] - top_left_point[1]) + 2 * (top_left_point[1] - top_left_point_diagonal[1])
x_offset = top_left_point[0] - top_left_point_diagonal[0]
y_offset = top_left_point[1] - top_left_point_diagonal[1]

top_left_pixel = (top_left_point[0] + pixel_width/2, top_left_point_diagonal[1] + pixel_height/2)

board_bounds = [
    [None] * 5,
    [None] * 6,
    [None] * 7,
    [None] * 8,
    [None] * 9,
    [None] * 8,
    [None] * 7,
    [None] * 6,
    [None] * 5
]

for i, row in enumerate(board_bounds):
    for j, pixel in enumerate(board_bounds[i]):
        modified_x_offset = (-abs(i-4)+4) * x_offset + j * pixel_width
        modified_y_offset = i*y_offset + i*(pixel_height/2)
        center_x = top_left_pixel[0] + modified_x_offset
        center_y = top_left_pixel[1] + modified_y_offset
        board_bounds[i][j] = (int(center_x - pixel_width/2), int(center_y - pixel_height/2), int(center_x + pixel_width/2), int(center_y + pixel_height/2))

board_bbox = (board_bounds[4][0][0], board_bounds[0][0][1], board_bounds[4][8][2], board_bounds[8][0][3])

board_strings = None
click_list = None

def print_formatted_board():
    for i, row in enumerate(board_strings):
        print(" " * abs(i-4), end="")
        for cell in row:
            print(f"{cell} ", end="")
        print()

def print_click_list():
    for i, row in enumerate(click_list):
        print(" " * abs(i-4), end="")
        for bool in row:
            print(f"{str(bool)[:1]} ", end="")
        print()

def toggle_string(i, j):
    if i < 0 or j < 0:
        raise IndexError("list index out of range (negative index)")

    global board_strings
    board_strings[i][j] = "X" if board_strings[i][j] == "O" else "O"

def simulate_click(i, j):
    try:
        global click_list
        click_list[i][j] = not click_list[i][j]
    except IndexError:
        return
    
    toggle_string(i, j)

    if i < 4:
        try:
            toggle_string(i, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j)
        except IndexError:
            pass
        try:
            toggle_string(i, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j)
        except IndexError:
            pass
    elif i == 4:
        try:
            toggle_string(i, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j)
        except IndexError:
            pass
    elif i > 4:
        try:
            toggle_string(i, j+1)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j)
        except IndexError:
            pass
        try:
            toggle_string(i+1, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i, j-1)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j)
        except IndexError:
            pass
        try:
            toggle_string(i-1, j+1)
        except IndexError:
            pass

def bring_down_tiles():
    for i, row in enumerate(board_strings):
        if i < 4:
            for j, pixel in enumerate(row):
                if pixel == "X":
                    simulate_click(i+1, j+1)
        if i >= 4:
            for j, pixel in enumerate(row):
                if pixel == "X":
                    simulate_click(i+1, j)

# from https://github.com/LegoFigure11/legofigure11.github.io/blob/master/fr/glimmer-and-gloom/index.html
def propagate():
    check_pixels = (
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (7, 5), (6, 6), (5, 7), (4, 8)
    )

    inputs = [board_strings[coord[0]][coord[1]] == "X" for coord in check_pixels]

    patterns = (
      (0, 0, 0, 1, 0, 1, 0, 0, 1),
      (0, 0, 0, 0, 1, 1, 1, 1, 0),
      (0, 0, 1, 1, 0, 1, 0, 1, 0),
      (1, 0, 1, 1, 0, 1, 1, 1, 1),
      (0, 1, 0, 0, 1, 0, 0, 1, 0),
      (1, 1, 1, 1, 0, 1, 1, 0, 1),
      (0, 1, 0, 1, 0, 1, 1, 0, 0),
      (0, 1, 1, 1, 1, 0, 0, 0, 0),
      (1, 0, 0, 1, 0, 1, 0, 0, 0),
    )

    solutions = []
    for i in range(9):
        solution = []
        for j in range(9):
            solution.append(patterns[j][i] if inputs[i] else 0)
        solutions.append(solution)

    final = [0] * 9
    for i in range(9):
        for j in range(9):
            final[i] += solutions[j][i]
        final[i] &= 1

    coords = (
        (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4)
    )

    for i, val in enumerate(final):
        if val == 1:
            simulate_click(coords[i][0], coords[i][1])

def solve_board():
    global board_strings, click_list
    board_strings = [
        [None] * 5,
        [None] * 6,
        [None] * 7,
        [None] * 8,
        [None] * 9,
        [None] * 8,
        [None] * 7,
        [None] * 6,
        [None] * 5
    ]

    click_list = [
        [False] * 5,
        [False] * 6,
        [False] * 7,
        [False] * 8,
        [False] * 9,
        [False] * 8,
        [False] * 7,
        [False] * 6,
        [False] * 5
    ]

    for i, row in enumerate(board_bounds):
        for j, pixel in enumerate(board_bounds[i]):
            image = ImageGrab.grab(board_bounds[i][j])
            if pyautogui.locate(os.path.join(dirname, "glimmer.png"), image, confidence=config["confidence"]):
                board_strings[i][j] = "X"
            elif pyautogui.locate(os.path.join(dirname, "gloom.png"), image, confidence=config["confidence"]):
                board_strings[i][j] = "O"
            else:
                print(f"Failed to find pixel ({i}, {j})")

    print_formatted_board()

    bring_down_tiles()

    propagate()

    bring_down_tiles()

    print("--------------")
    print_click_list()
    
    board_image = ImageGrab.grab(bbox=board_bbox)

    board_image = cv2.cvtColor(numpy.array(board_image), cv2.COLOR_RGB2BGR)

    for i, row in enumerate(click_list):
        for j, pixel in enumerate(row):
            if pixel:
                point1 = (board_bounds[i][j][0] - board_bbox[0] + int(pixel_width/3.6), board_bounds[i][j][1] - board_bbox[1] + int(y_offset))
                point2 = (board_bounds[i][j][2] - board_bbox[0] - int(pixel_width/3.6), board_bounds[i][j][3] - board_bbox[1] - int(y_offset))
                board_image = cv2.rectangle(board_image, point1, point2, (0, 0, 255), 4)

    board_image = Image.fromarray(cv2.cvtColor(board_image, cv2.COLOR_BGR2RGB))

    board_image = board_image.resize((int(board_image.size[0]/1.5), int(board_image.size[1]/1.5)))
    board_image = ImageTk.PhotoImage(board_image)
    image_label.config(image=board_image)
    image_label.image = board_image

gui = tkinter.Tk()
gui.geometry(f"{int((board_bbox[2]-board_bbox[0])/1.5) + 20}x{int((board_bbox[3]-board_bbox[1])/1.5) + 40}")
gui.title("G&G Very Hard Solver by TheFatRabbit")
gui.attributes("-topmost", True)

image_label = tkinter.Label(gui, image=None)
image_label.pack()

solve_button = tkinter.Button(gui, text="Solve Board", command=solve_board)
solve_button.pack()

keyboard.add_hotkey(config["hotkey"], solve_board)

gui.mainloop()