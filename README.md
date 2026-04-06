# Rock Paper Scissors - Hand Gesture Game 🎮

A Python-based Rock Paper Scissors game with real-time hand gesture detection using OpenCV and MediaPipe.

## Features

✊ **Rock** - Make a closed fist  
✋ **Paper** - Open your hand with all fingers extended  
✌️ **Scissors** - Two fingers extended (index and middle)  

- Real-time hand detection via webcam
- Live gesture classification
- Score tracking across multiple rounds
- Visual feedback with hand landmarks
- Play against the computer AI

## Installation

### Step 1: Create a virtual environment (recommended)

```bash
python3 -m venv venv
```

Activate the virtual environment:

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the game:

```bash
python game.py
```

## Controls

| Key | Action |
|-----|--------|
| **SPACE** | Throw your gesture (play round) |
| **R** | Reset game (clear all scores) |
| **Q** | Quit game |

## How to Play

1. Run `python game.py`
2. Allow camera access
3. Make a hand gesture:
   - **✊ ROCK**: Close your hand into a fist
   - **✋ PAPER**: Open your hand with all fingers spread
   - **✌️ SCISSORS**: Show two fingers (index and middle)
4. Press **SPACE** to throw when you see your gesture detected
5. The game will show the countdown and result
6. Press **SPACE** again after seeing the result to continue to the next round

## Game Flow

- **Detecting Phase**: Camera shows your hand and detects your gesture in real-time
- **Countdown Phase**: Dramatic 3-second countdown before the result is revealed
- **Result Phase**: Shows both choices and who won
- **Automatic Progression**: Game automatically moves to next round after 5 seconds

## Troubleshooting

### Camera not detected
- Make sure no other app is using your camera
- Check camera permissions on your system
- Try a different USB camera if available

### Gesture not detecting correctly
- Make sure your hand is clearly visible
- Try moving closer to the camera
- Ensure good lighting conditions
- Hold gestures steadily for detection

### Performance issues
- Close other applications to free up resources
- Reduce brightness/contrast settings if needed

## File Structure

```
rock_paper_scissors_game/
├── game.py              # Main game script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.7+
- Webcam/Camera
- opencv-python
- mediapipe
- numpy
