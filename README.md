# Rock Paper Scissors - Hand Gesture Game

A real-time **Rock Paper Scissors** game built with **Python**, **OpenCV**, and **MediaPipe Tasks**, where you play against the computer using **hand gestures detected from your webcam**. The application tracks your hand landmarks live, classifies your gesture, and runs a full round-based game loop with scorekeeping and on-screen feedback.

---

**Latest playable build:** available in the **Releases** section.

## Overview

This project uses your webcam to detect one hand in real time and classify it as **rock**, **paper**, or **scissors** based on finger positions. It combines computer vision with a simple game loop so you can play naturally in front of the camera instead of using buttons or keyboard-only input.

The project is built on the **MediaPipe Hand Landmarker Tasks API**, which requires a `.task` model file provided through `BaseOptions(model_asset_path=...)`, and uses OpenCV for webcam capture and rendering.

---

## Features

- Real-time webcam capture using OpenCV.
- Hand landmark detection with MediaPipe Hand Landmarker.
- Gesture classification for:
  - **Rock** — closed fist
  - **Paper** — open hand
  - **Scissors** — index and middle fingers extended
- Live visual feedback with hand landmarks drawn on screen.
- Score tracking for player wins, computer wins, and draws.
- Keyboard controls for playing, resetting, and quitting.
- Round-based gameplay against a random computer opponent.

---

## Demo Gameplay

1. Launch the game.
2. Show your hand to the webcam.
3. Wait until your gesture is detected on screen.
4. Press **SPACE** to throw your move.
5. The computer chooses its move automatically.
6. The game displays the result and updates the score.

---

## Tech Stack

- **Python**
- **OpenCV** for webcam capture and display.
- **MediaPipe Tasks** for hand landmark detection and trackin.
- **NumPy** for numerical operations.

---

## Project Structure

```text
rock_paper_scissors/
├── game.py                  # Main game script
├── hand_landmarker.task     # MediaPipe hand landmarker model
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .gitignore               # Git ignore rules
```

---

## Requirements

- Python **3.7+**
- A working **webcam**
- Windows, Linux, or macOS
- The following Python packages:
  - `opencv-python`
  - `mediapipe`
  - `numpy`

> Recommended tested dependencies:
>
> - `opencv-python==4.8.1.78`
> - `mediapipe==0.10.8`
> - `numpy==1.24.3`

---

## Download and Play

Want to play without setting up Python?

1. Open the **Releases** page of this repository.
2. Download the latest packaged version for Windows, for example:
   - `rock_paper_scissors_windows.zip`
3. Extract the zip file to a folder on your computer.
4. Open the extracted folder.
5. Double-click `rock_paper_scissors.exe` to launch the game.

> **Note**
> Please download the packaged file from **Releases**.
> Do **not** use the **Download ZIP** button from the main repository page, because that downloads the source code, not the ready-to-run application.

---

## OR Installation

### 1) Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rock_paper_scissors.git
cd rock_paper_scissors
```

### 2) Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Download the MediaPipe model file

This project requires the **MediaPipe Hand Landmarker** model file:
_It should be on the repo, but you can update it._

- `hand_landmarker.task`

Official model download:
`https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`

Place the file in the root project folder, next to `game.py`:

```text
rock_paper_scissors/
├── game.py
├── hand_landmarker.task
└── ...
```

The MediaPipe Python Hand Landmarker documentation shows that the task must be initialized with a model path through `BaseOptions(model_asset_path=...)`.

---

## Usage

Run the game with:

```bash
python game.py
```

If everything is configured correctly, the webcam window should open and start detecting your hand in real time. OpenCV uses `VideoCapture()` for webcam access, so your camera must be available and permitted by your operating system.

---

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Throw your current gesture / continue to next round |
| `R` | Reset the game and clear the score |
| `Q` | Quit the game |

---

## How to Play

1. Start the game with `python game.py`.
2. Make sure your webcam is active.
3. Hold one of the following gestures in front of the camera:
   - **Rock**: closed fist
   - **Paper**: open hand
   - **Scissors**: two fingers extended
4. Wait for the game to recognize the gesture.
5. Press **SPACE** to play the round.
6. The game compares your move with the computer’s move.
7. The score updates automatically.
8. Continue to the next round or reset at any time.

---

## Game Phases

### Detecting Phase

The application reads webcam frames continuously, detects one hand, and classifies the visible gesture in real time. MediaPipe provides hand landmarks for each frame, which are then interpreted by the game logic.

### Countdown Phase

After you throw your move, the game enters a short countdown before showing the result.

### Result Phase

The game displays:

- Your move
- The computer’s move
- The result of the round
- The updated score

---

## Troubleshooting

### Camera does not open

- Make sure no other application is using the webcam.
- Check your operating system camera permissions.
- Try restarting the app.
- On Windows, webcam access problems can also come from OS privacy settings blocking camera access for desktop apps.

### MediaPipe model error

If you see an error related to `ExternalFile` or model initialization, it usually means the file `hand_landmarker.task` is missing or the path is incorrect. The Hand Landmarker Tasks API requires a valid model file path in `BaseOptions(model_asset_path=...)`.

### Gesture is not recognized

- Keep your hand fully visible in the frame.
- Use good lighting.
- Avoid cluttered backgrounds.
- Hold the gesture still for a moment.
- Make sure only one hand is visible.

### The game opens but does not react

If the webcam window opens but the game does not detect playable gestures, the issue is usually in landmark interpretation or gesture classification rather than the camera itself. The Hand Landmarker returns per-frame hand landmarks, which your gesture logic must map correctly to rock, paper, and scissors.

---

## Packaging as an Executable

You can package the game as a Windows executable using **PyInstaller**. PyInstaller can bundle Python applications so they run on another Windows machine without requiring a separate Python installation.

### Example build command

```bash
pyinstaller --onedir --console --name rock_paper_scissors --add-data "hand_landmarker.task;." --collect-data mediapipe game.py
```

This generates a distributable app folder in `dist/`. For dependency-heavy apps like MediaPipe + OpenCV, a one-folder build is often easier to debug and more reliable than a one-file executable.

---

## Future Improvements

- Better gesture classification accuracy
- Start menu / UI overlay
- Sound effects and animations
- Difficulty modes
- Best-of-three or tournament mode
- Better packaging and installer support

---

## License

```text
MIT License
```

---

## Acknowledgments

- **MediaPipe** for real-time hand landmark detection.
- **OpenCV** for webcam capture and rendering.

---

## Author

Created by **XLS.studio**.
