import cv2
import mediapipe as mp
import numpy as np
import argparse
import time

#python pose_estimation.py --video push.mp4 -o output.mp4  
def parse_args():
    parser = argparse.ArgumentParser(
        description='Testing for Handstand.')
    parser.add_argument('-v', '--video', type=str, default='Squats.mp4')
    parser.add_argument('-o', '--output', type=str, default=None)
    parser.add_argument('--det', type=float, default=0.5, help='Detection confidence')
    parser.add_argument('--track', type=float, default=0.5, help='Tracking confidence')
    parser.add_argument('-wt', '--workout_type', type=str, default='PushUp')
    parser.add_argument('-c', '--complexity', type=int, default=0, help='Complexity of the model options 0,1,2')
    return parser.parse_args()

args = parse_args()
line_color = (255, 255, 255)
start_time = time.time()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=4, color=line_color)
detection_confidence = args.det
tracking_confidence = args.track
complexity = args.complexity
workout_type = args.workout_type

# Push-up tracking setup
up_pos = None
down_pos = None
pushup_pos = None
display_pos = None
push_up_counter = 0

vid = cv2.VideoCapture(args.video)
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(vid.get(cv2.CAP_PROP_FPS))
codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter(args.output, codec, fps, (width, height))

with mp_pose.Pose(
    min_detection_confidence=detection_confidence,
    min_tracking_confidence=tracking_confidence,
    model_complexity=complexity,
    smooth_landmarks=True
) as pose:
    while vid.isOpened():
        success, image = vid.read()
        if not success:
            break
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image.shape
        image.flags.writeable = True
        results = pose.process(image)

        try:
            landmarks = results.pose_landmarks.landmark
            left_eye = [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]
            right_eye = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            midpoint_shoulder_x = (int(shoulder[0] * image_width) + int(shoulder_r[0] * image_width)) / 2
            midpoint_shoulder_y = (int(shoulder[1] * image_height) + int(shoulder_r[1] * image_height)) / 2
            midpoint_hip_x = (int(left_hip[0] * image_width) + int(right_hip[0] * image_width)) / 2
            midpoint_hip_y = (int(left_hip[1] * image_height) + int(right_hip[1] * image_height)) / 2

            left_arm_angle = int(calculate_angle(shoulder, elbow, wrist))
            right_arm_angle = int(calculate_angle(shoulder_r, elbow_r, wrist_r))

            if workout_type == 'PushUp':
                if left_arm_angle > 160:
                    up_pos = 'Up'
                    display_pos = 'Up'
                if left_arm_angle < 110 and up_pos == 'Up':
                    down_pos = 'Down'
                    display_pos = 'Down'
                if left_arm_angle > 160 and down_pos == 'Down':
                    pushup_pos = "up"
                    display_pos = "up"
                    push_up_counter += 1
                    up_pos = None
                    down_pos = None
                    pushup_pos = None

            cv2.putText(image, f"Push-ups: {push_up_counter}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        except Exception as e:
            print("Error in pose tracking:", e)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, drawing_spec, drawing_spec)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        out.write(image)
        cv2.imshow('Exercise Tracker', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

vid.release()
out.release()
cv2.destroyAllWindows()