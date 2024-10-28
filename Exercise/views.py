
from django.shortcuts import render, redirect , get_object_or_404
from .models import Exercise
from .forms import ExerciseForm
from django.http import JsonResponse


def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'exercise_form.html', {'form': form})

def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercise_list.html', {'exercises': exercises})

def update_exercise(request, pk):
    exercise = Exercise.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('exercise_list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'exercise_form.html', {'form': form})

def delete_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.delete()
        return JsonResponse({'success': True, 'message': 'Exercise deleted successfully!'})
    return JsonResponse({'success': False, 'message': 'Failed to delete exercise.'})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    return render(request, 'exercise.html', {'exercise': exercise})

# the ai 
import cv2
import mediapipe as mp
import numpy as np
from django.http import StreamingHttpResponse

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
workout_type = 'PushUp'


# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle if angle <= 180 else 360 - angle

# Generator function to yield video frames with push-up count
def video_stream():
    vid = cv2.VideoCapture(0)
    push_up_counter = 0
    up_pos, down_pos, pushup_pos , display_pos = None, None , None, None


    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7, model_complexity=0 , smooth_landmarks=True) as pose:
        while vid.isOpened():
            success, image = vid.read()
            if not success:
                break

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = True
            image_height, image_width, _ = image_rgb.shape
            results = pose.process(image_rgb)
            
            if results.pose_landmarks:
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

            # Draw landmarks and counter
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS ,mp_drawing.DrawingSpec(color=(245, 117, 16), thickness=2, circle_radius=2),
                                 mp_drawing.DrawingSpec(color=(245, 117, 16), thickness=2, circle_radius=2))
            cv2.putText(image, f"Push-ups: {push_up_counter}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    vid.release()

# Django view to return StreamingHttpResponse
def pushup_counter_view(request):
    return StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')
