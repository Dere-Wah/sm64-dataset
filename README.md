# sm64-dataset
Collecting a dataset of SM64 gameplay. The dataset consists of combinations of game frames &amp; player inputs.

# Collecting Data
To create your own dataset, simply clone this repo and install the requirements.

```
pip install -r requirements.txt
```

Drag your compiled copy of SM64EX in the root folder of the repository.
> For more information on SM64EX, visit their official repository: https://github.com/sm64pc/sm64ex/wiki/Compiling-on-Windows



Run SM64 once and take note of the name of the window it opens. It should look something like:

```
Super Mario 64 EX (OpenGL) nightly 20bb444
```
> (The nightly build version will be probably different)

Open the config.yaml and complete it accordingly to your needs. This dataset aims at collecting data at a resolution of 320x240 frames.
By default, it will capture screenshots of the game at 1280x960 and compress them down to the target resolution. If you want to play around with these values and contribute to the dataset, make sure the aspect ratio is 4/3 and the target resolution is 320x240.

Finally, run the capture_data.py script. The script will launch the game for you and will start logging keypresses & screenshots.

```
python capture_data.py
```

To stop the game, simply press ESC.

# Keybinds Logging
When the game is running, a specific set of keypresses will be logged. Each keypress is mapped to a position in a vector, as shown below:

| forward | left | backward | right | crouch | jump | attack | camera up       | camera down       | camera left       | camera right       |
|---------|------|----------|-------|--------|------|--------|-----------------|-------------------|-------------------|--------------------|
| w       | a    | s        | d     | k      | l    | ,      | up              | down              | left              | right              |
| 0       | 1    | 2        | 3     | 4      | 5    | 6      | 7               | 8                 | 9                 | 10                 |

The number under the keybind is the position of the corresponding action in the vector.
When playing, you'll see the vector be printed in the terminal, so you can make sure that the keybinds are getting registered.

For special keybinds such as the arrow keys, you can use the "up", "down", "left" and "right" keywords.
> For a list of keywords you can use check out the pynput keyboard.Key enums: https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
Joystick support is on its way!

# Dataset Format
This dataset holds a really specific format, which allows for easier use in AI training. Once you run the script, you will find a new output folder generated, with inside it a list of .hdf5 files.
The hdf5 files contain each a list of 1000 captured frames (0 <= i <= 999), in the format:
- `frame_<i>_x`: the image data. 3 channels (BGR no alpha) at a resolution of target_resolution (320x240)
- `frame_<i>_y`: the key input data. Currently we log 11 actions, so it's an array of 0 and 1 of length 11.


# TO BE DONE
- [x] Create a configuration file
- [x] Add explanation for keybinds
- [x] Different keybinds support
- [ ] Joystick support
- [x] Document the output format
- [ ] Create a way for people to contribute to the dataset

