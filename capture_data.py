import time
import cv2
import mss
import numpy as np
import json
import os
import subprocess
from pynput import keyboard
import win32gui
import win32con
import h5py
import datetime

# Game executable path and arguments
game_path = "sm64.us.f3dex2e.exe"
game_args = ["--skip-intro", "--savepath", "!"]
sm64_ex_name = "Super Mario 64 EX (OpenGL) nightly 20bb444"

# Initialize some variables
frames_data = []
keys_pressed = []
output_dir = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
capture_interval = 0.05	# Capture every 0.05 seconds
target_width, target_height = 280, 210	# Desired window size
play_width, play_height = 1280, 960
# Define the specific keys we want to log
valid_keys = ['w', 'a', 's', 'd', 'k', 'l', ',', 
			  keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]
t = 0
file_prefix = output_dir
file_index = 0
			  
for key in enumerate(valid_keys):
	keys_pressed.append(0)

# Define the key press handlers
def on_press(key):
	if hasattr(key, 'char') and key.char in valid_keys:
		position = valid_keys.index(key.char)
		keys_pressed[position] = 1
	elif key in valid_keys:
		position = valid_keys.index(key)
		keys_pressed[position] = 1

def on_release(key):
	if hasattr(key, 'char') and key.char in valid_keys:
		position = valid_keys.index(key.char)
		keys_pressed[position] = 0
	elif key in valid_keys:
		position = valid_keys.index(key)
		keys_pressed[position] = 0
	if key == keyboard.Key.esc:
		return False  # Stop listener on ESC

# Function to get game window handle
def get_window_handle(window_name):
	hwnd = win32gui.FindWindow(None, window_name)
	if hwnd:
		win32gui.SetForegroundWindow(hwnd)
	return hwnd

# Function to set the window size
def set_window_size(hwnd, width, height):
	if hwnd:
		# Get the current position of the window
		rect = win32gui.GetWindowRect(hwnd)
		x, y = rect[0], rect[1]	 # Top-left corner
		
		# Move and resize the window
		win32gui.MoveWindow(hwnd, x, y, width, height, True)
	else:
		print("Failed to find window handle for resizing.")
		
def make_window_borderless(hwnd):
    if hwnd:
        # Get current window style
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        # Modify the style to remove the title bar and borders
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style & ~win32con.WS_OVERLAPPEDWINDOW)
        # Refresh the window with new style
        win32gui.SetWindowPos(hwnd, None, 0, 0, play_width, play_height, 
                              win32con.SWP_FRAMECHANGED | win32con.SWP_NOZORDER | win32con.SWP_NOMOVE)
    else:
        print("Failed to find window handle for borderless mode.")

# Capture frame from game window
def capture_frame(window_rect, h5file):
	global t
	global file_index
	if not window_rect:
		print("No valid game window. Exiting.")
		return False
	
	# Capture the game window region only
	with mss.mss() as sct:
		screenshot = sct.grab(window_rect)
		img = np.array(screenshot)
		
		# Convert from BGRA to BGR (OpenCV format)
		img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
		img = cv2.resize(img, (target_width, target_height))
		cv2.imwrite(f"{output_dir}/frame_{t}.png", img)
		
		h5file.create_dataset("frame_"+str(t)+"_x", data=img)
		h5file.create_dataset("frame_"+str(t)+"_y", data=list(keys_pressed))
		print(list(keys_pressed))

	t += 1
	return True

# Main function
def main():
	global t
	global file_index
	# Launch the game with the specified flags
	print("Launching the game...")
	game_process = subprocess.Popen([game_path] + game_args)
	time.sleep(3)  # Give the game some time to load

	# Get the game window handle and set the size
	hwnd = get_window_handle(sm64_ex_name)	# Replace with the exact game window title
	set_window_size(hwnd, play_width, play_height)
	make_window_borderless(hwnd)

	# Update the window capture region
	window_rect = win32gui.GetWindowRect(hwnd)
	window_rect = {'top': window_rect[1]+8, 'left': window_rect[0]+8, 
				   'width': play_width-8, 'height': play_height-8}

	# Ensure output directory exists
	os.makedirs(output_dir, exist_ok=True)
	
	
	h5file_name = file_prefix+"_"+str(file_index)+".hdf5"
	h5file = h5py.File(output_dir+"/"+h5file_name, 'w')	

	# Start keyboard listener
	listener = keyboard.Listener(on_press=on_press, on_release=on_release)
	listener.start()

	print("Starting capture... Press ESC to stop.")
	
	try:
		while listener.is_alive() and game_process.poll() is None:
			if not capture_frame(window_rect, h5file):
				break
			time.sleep(capture_interval)
			if t > 999:
				file_index += 1
				h5file.close()
				h5file_name = file_prefix+"_"+str(file_index)+".hdf5"
				h5file = h5py.File(output_dir+"/"+h5file_name, 'w')	
				t = 0
				print("Saving hdf5 file and skipping to next...")
	except KeyboardInterrupt:
		print("Capture stopped.")

	game_process.terminate()
	
	h5file.close()

	print("Data saved.")

if __name__ == "__main__":
	main()
