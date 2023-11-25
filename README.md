# Glimmer and Gloom Very Hard Solver
A solver for the Very Hard difficulty of the Glimmer and Gloom minigame on Flight Rising

Upon pressing a button or a customizable hotkey, the solver will search specific bounds for occurrences of both glimmer and gloom tiles and calculate the clicks required to solve the board from its curret state. The program will then overlay an indicator onto all tiles that need to be clicked in order to solve the board.

---

# Setup
Clone this repository. See this link if you need help: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository

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
    - Confidence: a value on the interval `[0, 1]` that states how close your screenshot must be to the detected tiles in order for the program to detect the board state
    - Screen bounding box in the form (x<sub>1</sub>, y<sub>1</sub>, x<sub>2</sub>, y<sub>2</sub>) following the image below
        - I suggest using MPos (https://sourceforge.net/projects/mpos/) to find your mouse position
<p align="center"><img height="300" src="https://i.imgur.com/Ypx7hfc.png"></p>

# Screenshots
- In the same environment as the one you will play G&G in, take a screenshot of the glimmer and gloom tiles, while leaving some space on each side. Name them `glimmer.png` and `gloom.png` and replace the current example files.

**You should be ready to run the program!**

To run the program without the command prompt, run `very_hard_solver.pyw`. It will terminate when you close the gui.
If you encounter any problems, create an issue.

# Personalizing
- Because board scaling may be different on each device, you may need to change the pixel locations slightly in order to account for such differences. The easiest way to do this is by temporarily commenting out line 265 (change the line's contents from `if pixel:` to `# if pixel:`) in order to outline all pixels regardless of whether or not they need to be clicked. Then, adjust the proportions on lines 17-20 as needed. Once the proportions are to your liking, uncomment line 265.  If the proportions of your game are vastly different from mine, smaller images in addition to the above modifications may lead to more reliable detection.