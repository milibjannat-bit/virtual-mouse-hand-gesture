import util
import json
import cv2
import mediapipe as mp
import pyautogui
import random
import time
import numpy as np 
from pynput.mouse import Button,Controller
from pathlib import Path

mpHands=mp.solutions.hands
screen_width, screen_height = pyautogui.size()
mouse=Controller()
last_action_time=0
control_enabled=False #Etat du contrôle :actif ou en veille
prev_x, prev_y=None, None 
save_dir = Path.home() / "Pictures" / "hand-mouse-screenshots"
save_dir.mkdir(parents=True, exist_ok=True)
MARGIN_X = 0.2
MARGIN_TOP = 0.2
MARGIN_BOTTOM = 0.35
DEFAULT_CONFIG={
    "smoothing":5,
    "move_thumb_dist":70,
    "toggle_threshold":70,
    "toggle_delay":1.5,
    "click_delay":0.5
}
CONFIG_PATH=Path(__file__).parent/"config.json"
def load_config():
    config = DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        print("config.json introuvable : valeurs par défaut utilisées.")
    except json.JSONDecodeError as e:
        print(f"config.json invalide ({e}) : valeurs par défaut utilisées.")
    return config
config = load_config()
SMOOTHING=config["smoothing"]
MOVE_THUMB_DIST=config["move_thumb_dist"]
toggle_threshold=config["toggle_threshold"]
TOGGLE_DELAY=config["toggle_delay"]
CLICK_DELAY=config["click_delay"]


hands =mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1 
) 
def can_act(delay):
    global last_action_time
    now = time.time()
    if now - last_action_time > delay:
        last_action_time = now
        return True
    return False

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks=processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None
def is_toggle_gesture(landmark_list):
    distance=util.get_distance([landmark_list[4],landmark_list[8]])
    if distance is None :
        return False
    middle_extended = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90
    return distance<toggle_threshold and middle_extended

        
def is_left_click(landmarks_list,thumb_index_dist):
    return(util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])<50 and 
          util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12])>90 and
          thumb_index_dist>50
    )

def is_right_click (landmarks_list,thumb_index_dist):
    return(util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12])<50 and 
              util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])>90 and
              thumb_index_dist>50
        )
def is_double_click(landmarks_list, thumb_index_dist):
    return(util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12])<50 and 
              util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])<50 and
              thumb_index_dist>50
        )
def screenshot(landmarks_list, thumb_index_dist):
    return(util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12])<50 and 
                  util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])<50 and
                  thumb_index_dist<50
            )

def move_mouse(index_finger_tip):
    global prev_x, prev_y
    if index_finger_tip is not None:
        x = int(np.interp(index_finger_tip.x, [MARGIN_X, 1 - MARGIN_X], [0, screen_width]))
        y = int(np.interp(index_finger_tip.y, [MARGIN_TOP, 1 - MARGIN_BOTTOM], [0, screen_height]))
        if prev_x is None :
            prev_x, prev_y=x, y
        smooth_x=prev_x+(x-prev_x)/SMOOTHING
        smooth_y=prev_y+(y-prev_y)/SMOOTHING
        pyautogui.moveTo(int(smooth_x),int(smooth_y))
        prev_x,prev_y=smooth_x,smooth_y

def detected_gestures(frame,landmarks_list,processed):
    global control_enabled
    if len(landmarks_list)>=21:
        index_finger_tip=find_finger_tip(processed)
        thumb_index_dist=util.get_distance([landmarks_list[4],landmarks_list[5]])
        index_angle = util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])
        cv2.putText(frame, f"dist={int(thumb_index_dist)} angle={int(index_angle)}", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        toggle_dist = util.get_distance([landmarks_list[4], landmarks_list[8]])
        cv2.putText(frame, f"toggle dist={int(toggle_dist)}", (50,140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        if is_toggle_gesture(landmarks_list):
            if can_act(TOGGLE_DELAY):
                control_enabled=not control_enabled
        elif control_enabled:
            if thumb_index_dist < MOVE_THUMB_DIST and util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90:
                move_mouse(index_finger_tip)
                cv2.putText(frame,"mouse is moving",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            #RICHT CLICK
            elif is_right_click(landmarks_list,thumb_index_dist):
                if can_act(CLICK_DELAY):
                   mouse.press(Button.right)
                   mouse.release(Button.right)
                cv2.putText(frame,"Right Click",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            #LEFT CLICK
            elif is_left_click(landmarks_list,thumb_index_dist):
                if can_act(CLICK_DELAY):
                   mouse.press(Button.left)
                   mouse.release(Button.left)  
                cv2.putText(frame,"Left Click",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            #DOUBLE CLICK      
            elif is_double_click(landmarks_list,thumb_index_dist):
                if can_act(CLICK_DELAY):
                  pyautogui.doubleClick()
                cv2.putText(frame,"Double Click",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 127, 0),2)
            elif screenshot(landmarks_list, thumb_index_dist):
                if can_act(2):
                  im1=pyautogui.screenshot()
                  label=random.randint(1,1000)
                  im1.save(f'my_screenshot_{label}.png')
                cv2.putText(frame,"screnshot Click",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(127,255, 0),2)

def main():
    cap=cv2.VideoCapture(0)
    draw=mp.solutions.drawing_utils
    try:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break
            frame=cv2.flip(frame,1)
            frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmarks_list=[]
            if processed.multi_hand_landmarks:
                hand_landmarks=processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame,hand_landmarks,mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x,lm.y))

            detected_gestures(frame,landmarks_list,processed)
            state_text = "Control ON" if control_enabled else "Control OFF"
            state_color = (0,255,0) if control_enabled else (0,0,255)
            cv2.putText(frame, state_text, (50,180), cv2.FONT_HERSHEY_SIMPLEX, 0.9, state_color, 2)

            cv2.imshow('Frame',frame)
            if cv2.waitKey(1)& 0xFF ==ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
if __name__=='__main__':
    main()
    