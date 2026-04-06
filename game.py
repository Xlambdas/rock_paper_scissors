import cv2
import mediapipe as mp
import random
import time
import numpy as np

class RockPaperScissorsGame:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

        # Game variables
        self.choices = ['rock', 'paper', 'scissors']
        self.player_score = 0
        self.computer_score = 0
        self.draw_score = 0
        self.round_number = 1

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Game state
        self.game_state = 'detecting'  # detecting, countdown, result, round_end
        self.detected_gesture = None
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.countdown = 0
        self.countdown_start_time = 0
        self.result_start_time = 0

    def classify_gesture(self, hand_landmarks):
        """Classify hand gesture based on landmarks"""
        if not hand_landmarks:
            return None

        lm = hand_landmarks.landmark

        # Get key positions
        thumb_tip = lm[4]
        index_tip = lm[8]
        middle_tip = lm[12]
        ring_tip = lm[16]
        pinky_tip = lm[20]

        # Get PIP (middle joint) positions
        index_pip = lm[6]
        middle_pip = lm[10]
        ring_pip = lm[14]
        pinky_pip = lm[18]
        thumb_pip = lm[3]

        # Count extended fingers (tip above pip = extended)
        extended_fingers = 0
        if index_tip.y < index_pip.y:
            extended_fingers += 1
        if middle_tip.y < middle_pip.y:
            extended_fingers += 1
        if ring_tip.y < ring_pip.y:
            extended_fingers += 1
        if pinky_tip.y < pinky_pip.y:
            extended_fingers += 1

        # Check thumb (different axis)
        thumb_extended = thumb_tip.x < thumb_pip.x

        # Classify gesture
        if extended_fingers == 0:
            return 'rock'  # Closed fist
        elif extended_fingers == 2:
            # Check if it's scissors (index and middle extended, others not)
            if (index_tip.y < index_pip.y and
                middle_tip.y < middle_pip.y and
                ring_tip.y > ring_pip.y and
                pinky_tip.y > pinky_pip.y):
                return 'scissors'
        elif extended_fingers >= 3:
            return 'paper'  # Most fingers extended

        return None

    def draw_info(self, frame, gesture, game_state):
        """Draw game information on frame"""
        h, w, c = frame.shape

        # Draw semi-transparent background for text
        overlay = frame.copy()

        # Draw scores at top
        score_text = f"You: {self.player_score} | Computer: {self.computer_score} | Draw: {self.draw_score}"
        cv2.putText(frame, score_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

        # Draw round number
        round_text = f"Round {self.round_number}"
        cv2.putText(frame, round_text, (w - 250, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

        # Draw current gesture detected
        if gesture and game_state == 'detecting':
            gesture_emoji = {'rock': 'rock', 'paper': 'paper', 'scissors': 'scissors'}.get(gesture, '?')
            cv2.putText(frame, f"Detected: {gesture.upper()} {gesture_emoji}", (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 200, 255), 2)

            # Draw ready indicator
            cv2.putText(frame, "Press SPACE to throw!", (20, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw countdown
        if game_state == 'countdown':
            elapsed = time.time() - self.countdown_start_time
            remaining = max(0, 3 - int(elapsed))
            cv2.putText(frame, str(remaining) if remaining > 0 else "GO!", 
                       (w // 2 - 40, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 3)

        # Draw result
        if game_state == 'result':
            elapsed = time.time() - self.result_start_time

            # Draw choices
            choice_text = f"You: {self.player_choice.upper()} vs Computer: {self.computer_choice.upper()}"
            cv2.putText(frame, choice_text, (w // 2 - 350, h // 2 - 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

            # Draw result with color
            if self.result == 'win':
                result_color = (0, 255, 0)
                result_text = "YOU WIN!"
            elif self.result == 'lose':
                result_color = (0, 0, 255)
                result_text = "COMPUTER WINS!"
            else:
                result_color = (0, 255, 255)
                result_text = "DRAW!"

            cv2.putText(frame, result_text, (w // 2 - 300, h // 2 + 50), cv2.FONT_HERSHEY_SIMPLEX, 2, result_color, 3)

            if elapsed > 3:
                cv2.putText(frame, "Press SPACE for next round!", (w // 2 - 300, h // 2 + 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2)

        # Draw instructions
        cv2.putText(frame, "ROCK PAPER SCISSORS - Hand Gesture Game", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 1)
        cv2.putText(frame, "Q: Quit | SPACE: Throw | R: Reset Game", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)

    def play_round(self):
        """Execute one round of the game"""
        if not self.detected_gesture:
            return

        self.player_choice = self.detected_gesture
        self.computer_choice = random.choice(self.choices)

        # Determine winner
        if self.player_choice == self.computer_choice:
            self.result = 'draw'
            self.draw_score += 1
        elif (self.player_choice == 'rock' and self.computer_choice == 'scissors') or \
                (self.player_choice == 'paper' and self.computer_choice == 'rock') or \
                (self.player_choice == 'scissors' and self.computer_choice == 'paper'):
            self.result = 'win'
            self.player_score += 1
        else:
            self.result = 'lose'
            self.computer_score += 1

        self.game_state = 'countdown'
        self.countdown_start_time = time.time()

    def reset_game(self):
        """Reset game scores and round"""
        self.player_score = 0
        self.computer_score = 0
        self.draw_score = 0
        self.round_number = 1
        self.game_state = 'detecting'
        self.detected_gesture = None
        self.player_choice = None
        self.computer_choice = None
        self.result = None

    def run(self):
        """Main game loop"""
        print("Rock Paper Scissors - Hand Gesture Game")
        print("=" * 50)
        print("Controls:")
        print("  SPACE - Throw your gesture")
        print("  R - Reset game")
        print("  Q - Quit")
        print("=" * 50)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Flip frame horizontally for selfie view
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape

            # Convert to RGB for MediaPipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            # Detect gesture
            self.detected_gesture = None
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                self.detected_gesture = self.classify_gesture(hand_landmarks)

                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # Update game state based on time
            if self.game_state == 'countdown':
                elapsed = time.time() - self.countdown_start_time
                if elapsed > 3:
                    self.game_state = 'result'
                    self.result_start_time = time.time()

            elif self.game_state == 'result':
                elapsed = time.time() - self.result_start_time
                if elapsed > 5:
                    self.round_number += 1
                    self.game_state = 'detecting'
                    self.player_choice = None
                    self.computer_choice = None
                    self.result = None

            # Draw info on frame
            self.draw_info(frame, self.detected_gesture, self.game_state)

            # Display frame
            cv2.imshow('Rock Paper Scissors Game', frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Thanks for playing! Final Scores:")
                print(f"You: {self.player_score} | Computer: {self.computer_score} | Draws: {self.draw_score}")
                break
            elif key == ord(' '):
                if self.game_state == 'detecting':
                    self.play_round()
                elif self.game_state == 'result' and time.time() - self.result_start_time > 3:
                    self.round_number += 1
                    self.game_state = 'detecting'
                    self.player_choice = None
                    self.computer_choice = None
                    self.result = None
            elif key == ord('r'):
                self.reset_game()
                print("Game reset!")

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()