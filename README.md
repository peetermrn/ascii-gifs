# Ascii-gifs aka spinningFish

Just for fun:). Animate gif as ascii art. GIFs in test_gifs are for testing.

Works in linux terminal and windows cmd but
not on windows git bash (ANSI escape sequence isn't
supported [from what i understood](https://github.com/microsoft/terminal/issues/6634) meaning clearing the terminal
between frames breaks).

---

### How it works

Loop through frames of GIF, convert each frame to greyscale meaning each pixel has a value between 0 and 1 depending on
the pixel's brightness. Next map each pixel value to an ascii character based on their brightness. Then just print out
resulting string and "voilà!" we have an ascii picture. Use ANSI escape codes to clear terminal between frames and
format
picture size depending on terminal size to fit image properly.

---

### Getting started (no install script yet)

1. clone `git clone https://github.com/peetermrn/ascii-gifs`
2. Install dependencies:
    3. Python version 3.6 or above
    4. PIL Pillow  `pip install Pillow`
5. Create alias for easier use
6. Create ascii GIFs:) (examples below)

---

### Example terminal uses

For linux:    
`python3 ascif.py test_gifs/fish.gif --loop --time_multiplier=1.5`    
For windows:    
`python ascif.py test_gifs\fish.gif --loop --time_multiplier=1.5`   
(arguments explained below)

- `--loop` adding this keeps the GIF looping
- `--time_multiplier=1.5` sets gif to run at 1.5x speed

![example_fish.gif](md_srcs%2Fexample_fish.gif)

For linux:    
`python3 ascif.py test_gifs/dance.gif --loop --time_multiplier=1.5 --more_detailed`    
For windows:    
`python ascif.py src_gifs\dance.gif --loop --time_multiplier=1.5 --more_detailed`     
(arguments explained below)

- `--loop` adding this keeps the GIF looping
- `--time_multiplier=2` sets gif speed to 2x
- `--more_detailed` sets color ballet do have 21 different colors

![example_dance.gif](md_srcs%2Fexample_dance.gif)

---

### Optional parameters explained

- `--loop` adding this keeps the GIF looping
- `--time_multiplier=` determines the gif speed (each frame playback rate). For example `--time_multiplier=2` would set
  the GIF to run at double the speed
- `--revser_colors` adding this reverses order of colors - black becomes white and white becomes black etc
- `--more_detailed` sets color schema do have 21 different colors instead of the default 11
