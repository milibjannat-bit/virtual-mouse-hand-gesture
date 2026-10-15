# virtual-mouse-hand-gesture
Control the mouse with hand gestures using OpenCV and MediaPipe# Virtual Mouse with Hand Gestures

Control your computer's mouse with your hand, using only a webcam. Built with Python, OpenCV and MediaPipe.

## Features

- Move the cursor by moving your hand in front of the camera
- Left click, right click and double click with finger gestures
- Take a screenshot with a gesture
- Smooth cursor movement (reduces hand-tracking jitter)
- Active zone: you can reach every edge of the screen without your hand leaving the camera image

## Gestures

| Action | Gesture |
|---|---|
| Move the cursor | Index and middle fingers extended, thumb close to the base of the index |
| Left click | Index finger bent, middle finger extended, thumb away |
| Right click | Middle finger bent, index finger extended, thumb away |
| Double click | Index and middle fingers both bent, thumb away |
| Screenshot | Index and middle fingers both bent, thumb close |

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

You can tune the behavior with the constants at the top of `main.py`:

| Constant | Role |
|---|---|
| `SMOOTHING` | Higher = steadier cursor but slower to follow your hand |
| `MOVE_THUMB_DIST` | How close the thumb must be to trigger cursor movement |
| `MARGIN_X`, `MARGIN_TOP`, `MARGIN_BOTTOM` | Part of the camera image ignored on each side (the active zone) |
| `CLICK_DELAY` | Minimum delay between two clicks, in seconds |

## Project structure

```
main.py             Main program: camera loop, gesture detection, mouse control
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

## License

MIT
