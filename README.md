# Glimmer and Gloom Very Hard Solver
A solver for the Very Hard difficulty of the Glimmer and Gloom minigame on Flight Rising

Upon pressing a button or a customizable hotkey, the solver will search specific bounds for occurrences of both glimmer and gloom tiles and calculate the clicks required to solve the board from its curret state. The program will then overlay an indicator onto all tiles that need to be clicked in order to solve the board.

<p align="center"><img height="300" src="https://i.imgur.com/Lc6Akm1.png"></p>

---

# Setup
Clone this repository. See this link if you need help: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository
You may need to install Git if you have not previously: https://git-scm.com/downloads

# Requirements
- Python (https://www.python.org/downloads/)
    - Pip (https://pip.pypa.io/en/stable/installation/) (should be preinstalled with Python)
    - Libraries:
        - Navigate to the project directory (in Command Prompt, type `cd <folder path>`)
        - Type the following command: `pip install -r requirements.txt`
You should now be ready to set up the `config.json` file

# Config
- In `config.json` set the following:
    - Preferred hotkey (must be a valid hotkey in the `keyboard` package)
    - If you wish for Light to win instead of Shadow, change `winner` from `gloom` to `glimmer`
    - Confidence: a value on the interval `[0, 1]` that states how close your screenshot must be to the detected tiles in order for the program to detect the board state
    - Screen bounding box in the form (x<sub>1</sub>, y<sub>1</sub>, x<sub>2</sub>, y<sub>2</sub>) following the image below
        - I suggest using MPos (https://sourceforge.net/projects/mpos/) to find your mouse position
<p align="center"><img height="300" src="https://i.imgur.com/Ypx7hfc.png"></p>

# Screenshots
- In the same environment as the one you will play G&G in, take a screenshot of the glimmer and gloom tiles, while leaving some space on each side. Name them `glimmer.png` and `gloom.png` and replace the current example files.

**You should be ready to run the program!**

To run the program without the command prompt, run `very_hard_solver.pyw`. It will terminate when you close the gui.
If you encounter any problems, create an issue.

# Personalizing & Troubleshooting
- Because board scaling may be different on each device, you may need to change the pixel locations slightly in order to account for such differences. The easiest way to do this is by temporarily commenting out the line that says `if pixel and ((j == 0 and i < 5) or (i == 0)):` (add `#` to the beginning of the line) in order to outline all pixels regardless of whether or not they need to be clicked. Then, adjust the `numerators` values in `config.json` as needed. These are ratios between specific points (see figure below) on the game board and the top left corner of Glimmer and Gloom, calculated from 0-700 on the x axis and 0-600 on the y axis (from the computer on which this program was developed). Often, by observing the error buildup of the location of each rectangle placed on the board, you can make the adjustments necessary to normalize the tool for your setup without measuring each value anew (but in extreme cases this may still need to be done). Once the proportions are to your liking, uncomment the line you commented out earlier.  If the proportions of your game are vastly different from mine, smaller images in addition to the above modifications may lead to more reliable detection.
```
"numerators": [
    [x1, y1],
    [x2, y2],
    [x3, y3],
    [x4, y4]
]
```
<p align="center"><img height="300" src="https://i.imgur.com/JdhLUYu.png"></p>