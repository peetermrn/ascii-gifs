# Ascii-gifs aka spinningFish

Just for fun:). Animate gif as ascii art. GIFs in test_gifs are for testing.

Works in linux terminal and windows cmd but
not on windows git bash (ANSI escape sequence isn't
supported [from what i understood](https://github.com/microsoft/terminal/issues/6634) meaning clearing the terminal
between frames breaks)


---

### Getting started (no install script yet)

1. clone `git clone https://github.com/peetermrn/ascii-gifs`
2. Install dependencies:
    3. Python version 3.6 or above
    4. PIL Pillow  `pip install Pillow`
5. Create alias for easier use
5. Create ascii GIFs:) (examples below)

---

### Example terminal uses

For linux:    
`python3 ascif.py src_gifs/dance.gif --loop --t=0.05 --more_detailed`    
For windows:    
`python ascif.py src_gifs\dance.gif --loop --t=0.05 --more_detailed`     
(arguments explained below)

- `--loop` adding this keeps the GIF looping
- `--t=` sets time between frames to 0.05 seconds
- `--more_detailed` sets color ballet do have 21 different colors

![example_1.gif](md_srcs%2Fexample_1.gif)
For linux:    
`python3 ascif.py test_gifs/fish.gif --loop --t=0.05`    
For windows:    
`python ascif.py test_gifs\fish.gif --loop --t=0.05`   
(arguments explained below)

- `--loop` adding this keeps the GIF looping
- `--t=` sets time between frames to 0.05 seconds

![example_2.gif](md_srcs%2Fexample_2.gif)

---

### Optional parameters explained

- `--loop` adding this keeps the GIF looping
- `--t=` sets time between frames, default is set to 0.01
- `--revser_colors` adding this reverses order of colors - black becomes white and white becomes black etc
- `--more_detailed` sets color schema do have 21 different colors instead of the default 11
