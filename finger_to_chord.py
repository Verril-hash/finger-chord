import cv2
import mediapipe as mp
import pygame

# Initialize Pygame Mixer for audio playback
pygame.mixer.init()

# Load chord sound files
g_chord = pygame.mixer.Sound("G_chord.wav.mp3")
d_chord = pygame.mixer.Sound("D_chord.wav.mp3")
c_chord = pygame.mixer.Sound("C_chord.wav.mp3")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Finger tip landmarks
finger_tips = [4, 8, 20]  # Thumb, Index, Little
thumb_tip = 4
index_tip = 8
pinky_tip = 20

# To avoid playing the same sound repeatedly
last_played = None

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            h, w, _ = frame.shape

            # Detect thumb, index and pinky finger states
            thumb_up = landmarks[thumb_tip].x < landmarks[thumb_tip - 1].x
            index_up = landmarks[index_tip].y < landmarks[index_tip - 2].y
            pinky_up = landmarks[pinky_tip].y < landmarks[pinky_tip - 2].y

            if thumb_up and last_played != "G":
                print("Playing G Chord")
                g_chord.play()
                last_played = "G"
            elif index_up and last_played != "D":
                print("Playing D Chord")
                d_chord.play()
                last_played = "D"
            elif pinky_up and last_played != "C":
                print("Playing C Chord")
                c_chord.play()
                last_played = "C"
            elif not (thumb_up or index_up or pinky_up):
                last_played = None

    cv2.imshow("Finger to Chord", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
