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
> (The nightly build version will be probably different, just update it)

Finally, run the capture_data.py script. The script will launch the game for you and will start logging keypresses & screenshots.

```
python capture_data.py
```

To stop the game, simply press ESC.

# TO BE DONE
- [ ] Create a configuration file
- [ ] Add explanation for keybinds
- [ ] Document the output format
- [ ] Create a way for people to contribute to the dataset

