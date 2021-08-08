import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.widgets import Button
from tkinter import *
from tkinter.messagebox import askyesno
#from tkinter.filedialog import askopenfilename, asksaveasfilename, asksaveasfile
from tkinter import filedialog
import json
class Shot:
    def __init__(self, made, x, y):
        self.made = made
        self.x = x;
        self.y = y;
def create_nba_court(ax, color):
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)

def save_shot_chart(shot_stack):
    #Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    save_file = filedialog.asksaveasfilename(initialfile = 'Untitled Shot Chart.json', confirmoverwrite=True, defaultextension='.json', filetypes=[("Json files *.json", "*.json")], title="Save Your Shot Chart file.") # show an "Open" dialog box and return the path to the selected file

    if not save_file:
        return
    #file = filedialog.asksaveasfile()
    # create pandas dataframe with series of: ID, Shot Made, X-coordinate, Y-coordinate
    dict = {'ID': [], 'Shot Made': [], 'X': [], 'Y': []}
    for tup in shot_stack:
        dict['ID'].append(tup[0])
        dict['Shot Made'].append(tup[1].made)
        dict['X'].append(tup[1].x)
        dict['Y'].append(tup[1].y)

    df = pd.DataFrame(dict)
    df.to_json(save_file)
# store coordinates as stack.
shot_stack = []
# General plot parameters
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2

shot_id = 0


def reset_ax():
    ax = fig.add_axes([0, 0, 1, 1])
    ax = create_nba_court(ax, 'black')
    return ax
# Draw basketball court
fig = plt.figure(figsize=(4, 3.76))
ax = reset_ax()

def undo_shot():
    global shot_id
    try:
        shot_stack.pop()
        shot_id -= 1
        plt.cla()
        ax = reset_ax()
        draw_shots()
    except: pass
def draw_shots():
    for tup in shot_stack:
        shot = tup[1]
        if shot.made:
            plt.plot(shot.x, shot.y, 'o', color='red')
        else:
            plt.plot(shot.x, shot.y, 'x', color='blue')
    fig.canvas.draw()

def clear_shot_chart():
    global shot_id
    plt.cla()
    ax = reset_ax()
    shot_stack.clear()
    shot_id = 0
    fig.canvas.draw()

def load_shot_chart():
    global shot_id
    # first ask if we really want to clear the current shot chart and load a json of a shot chart

    #Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    files = filedialog.askopenfilename(filetypes=[("Json File", "*.json")], title="Choose a Shot Chart file.", multiple=True) # show an "Open" dialog box and return the path to the selected file
    for file in files:
        print(file)

    # clear current figure and shot_stack
    # plt.cla()
    # ax = reset_ax()
    # shot_stack.clear()
    # shot_id = 0
    clear_shot_chart()
    # read json into shot_stack
    for file in files:
        with open(file) as json_file:
            dict = json.load(json_file)
            for i in range(len(dict['ID'])):
                str_i = str(i)

                shot_stack.append((shot_id, Shot(dict['Shot Made'][str_i], dict['X'][str_i], dict['Y'][str_i])))
                shot_id+=1
    draw_shots()
    #fig.canvas.draw()
def on_click(event):
    global shot_id
    if event.button is MouseButton.LEFT:
        shot_stack.append((shot_id, Shot(True, event.xdata, event.ydata)))

    if event.button is MouseButton.RIGHT:
        shot_stack.append((shot_id, Shot(False, event.xdata, event.ydata)))
    shot_id += 1

    draw_shots()

def confirm(message_text, action):
    root = Tk().withdraw()
    answer = askyesno(title='confirmation',
                message=message_text)
    if answer:
        if action == 'load':
            load_shot_chart()
        if action == 'clear':
            clear_shot_chart()

def on_press(event):
    if event.key == 'u':
        undo_shot()
    if event.key == 'j':
        save_shot_chart(shot_stack)
    if event.key == '0':
        confirm('Are you sure that you want to clear the current figure and load shot chart(s)?', 'load')
    if event.key == 'c':
        confirm('Are you sure that you want to clear the current figure?', 'clear')



plt.connect('button_press_event', on_click)
plt.connect('key_press_event', on_press)

plt.show()
