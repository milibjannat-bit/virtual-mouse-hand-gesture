# virtual-mouse-hand-gesture

Control your computer's mouse with your hand, using only a webcam. Built with Python, OpenCV and MediaPipe.

## Features

- Move the cursor by moving your hand in front of the camera
- Left click, right click and double click with finger gestures
- Take a screenshot with a gesture
- Smooth cursor movement (reduces hand-tracking jitter)
- Active zone: you can reach every edge of the screen without your hand leaving the camera image
- Toggle the control on and off with a pinch gesture (sleep mode, to avoid accidental actions)
- Scroll up and down by holding your hand above or below the position where you started the gesture

## Gestures

| Action | Gesture |
|---|---|
| Move the cursor | Index and middle fingers extended, thumb close to the base of the index |
| Left click | Index finger bent, middle finger extended, thumb away |
| Right click | Middle finger bent, index finger extended, thumb away |
| Double click | Index and middle fingers both bent, thumb away |
| Screenshot | Index and middle fingers both bent, thumb close |
| Toggle control ON/OFF | Thumb and index fingertips pinched together, middle finger extended |
| Scroll | Index and middle fingers extended, thumb wide open. Hold your hand higher than where you started to scroll up, lower to scroll down |

The program **starts in sleep mode** ("Control OFF"): the camera and hand detection run, but no cursor movement or click is sent. Pinch to switch to "Control ON". Pinch again to go back to sleep. The current state is always shown on screen.
Press `q` in the camera window to quit.

## How it works

1. OpenCV captures frames from the webcam.
2. MediaPipe Hands detects 21 landmarks (points) on the hand.
3. The program measures the angle of each finger joint and the distance between the thumb and the index finger to recognize the gesture.
4. PyAutoGUI and pynput move the cursor and trigger clicks.

## Installation

Requirements: Python 3.9 - 3.12 and a webcam.

```bash
git clone https://github.com/milibjannat-bit/virtual-mouse-hand-gesture.git
cd virtual-mouse-hand-gesture

python -m venv venv
venv\Scripts\activate        # Windows (PowerShell)
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Configuration

Most settings live in `config.json`, next to `main.py`. Edit the file and restart the program to apply your changes. If the file is missing or contains a syntax error, the program prints a message and uses the default values. A setting that is absent from the file also keeps its default.

| Setting | Role | Default |
|---|---|---|
| `smoothing` | Higher = steadier cursor but slower to follow your hand | 5 |
| `move_thumb_dist` | How close the thumb must be to trigger cursor movement | 70 |
| `toggle_threshold` | How close the thumb and index fingertips must be to count as a pinch (lower = tighter pinch needed) | 70 |
| `toggle_delay` | Minimum delay between two toggles, in seconds (prevents flickering while the pinch is held) | 1.5 |
| `click_delay` | Minimum delay between two clicks, in seconds | 0.5 |
| `scroll_thumb_dist` | How wide the thumb must be open to trigger scrolling | 200 |
| `scroll_delay` | Minimum delay between two scroll steps, in seconds (higher = slower scroll) | 0.1 |

The active zone margins (`MARGIN_X`, `MARGIN_TOP`, `MARGIN_BOTTOM`) and the scroll dead zone (`SCROLL_ZONE`) are constants defined at the top of `main.py`.

## Project structure

```
main.py             Main program: camera loop, gesture detection, mouse control
config.json         Settings: thresholds and delays
util.py             Helper functions (angle and distance between landmarks)
requirements.txt    Python dependencies
```

## Known limitations

- Works best with good lighting and one hand visible in the image.
- Screenshots are saved in the project folder as `my_screenshot_<number>.png`.

## Credits

Based on a YouTube tutorial: (https://www.youtube.com/watch?v=4NmwNEYtL1s).
Improvements added on top of the tutorial:
- Cursor smoothing
- Active zone with separate top/bottom margins
- More tolerant cursor-movement detection
- ON/OFF toggle gesture (sleep mode)
- Settings file (`config.json`) with default values
- Scroll gesture (direction given by the hand's height relative to a neutral point)
## License

MIT
