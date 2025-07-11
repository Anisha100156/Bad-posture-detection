import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """Calculate angle between three points with b as the vertex."""
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) -
                       math.atan2(a[1] - b[1], a[0] - b[0]))
    ang = abs(ang)
    if ang > 180:
        ang = 360 - ang
    return ang
def analyze_posture(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    feedback = []
    neck_angles = []
    back_angles = []
    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_num += 1
            frame = cv2.resize(frame, (640, 480))
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if not results.pose_landmarks:
                continue
            lm = results.pose_landmarks.landmark
            try:
                nose = lm[mp_pose.PoseLandmark.NOSE.value]
                left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP.value]
                right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
                left_knee = lm[mp_pose.PoseLandmark.LEFT_KNEE.value]
                right_knee = lm[mp_pose.PoseLandmark.RIGHT_KNEE.value]
                left_ankle = lm[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                left_toe = lm[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
                shoulder = ((left_shoulder.x + right_shoulder.x) / 2, (left_shoulder.y + right_shoulder.y) / 2)
                hip = ((left_hip.x + right_hip.x) / 2, (left_hip.y + right_hip.y) / 2)
                knee = ((left_knee.x + right_knee.x) / 2, (left_knee.y + right_knee.y) / 2)
                virtual_vertical = (shoulder[0], shoulder[1] - 0.03)
                neck_angle = calculate_angle((nose.x, nose.y), shoulder, virtual_vertical)
                back_angle = calculate_angle(shoulder, hip, knee)
                neck_angles.append(neck_angle)
                back_angles.append(back_angle)
                messages = []
                if neck_angle > 9:
                    messages.append(f"Neck bent by {neck_angle:.1f}° — keep your head upright.")
                else:
                    messages.append("🟢 Perfect neck posture.")
                if back_angle < 160:
                    messages.append(f"Back angle is {back_angle:.1f}° — sit straighter.")
                else:
                    messages.append("🟢 Good back posture.")
                if abs(left_knee.x - left_toe.x) > 0.05:
                    messages.append("Knee is beyond toe — fix squat stance.")
                else:
                    messages.append("🟢 Knee within safe range.")

                feedback.append(f"Frame {frame_num}: " + " | ".join(messages))
            except Exception as e:
                print(f"Error in frame {frame_num}: {e}")
                continue
    cap.release()
    good_frames = sum(
        1 for f in feedback if
        "🟢 Perfect neck posture." in f and
        "🟢 Good back posture." in f and
        "🟢 Knee within safe range." in f
    )
    avg_neck = sum(neck_angles) / len(neck_angles) if neck_angles else 0
    min_back = min(back_angles) if back_angles else 0
    summary = (
        f"Summary: {'🟢 Good job!' if good_frames > 0.7 * len(feedback) else '⚠️ Posture needs improvement.'} "
        f"Only {good_frames}/{len(feedback)} frames were fully correct.\n"
        f"💡Avg neck tilt: {avg_neck:.1f}° — try to keep it <9°.\n"
        f"🧘Min back angle: {min_back:.1f}° — aim for ≥160° for upright posture."
    )

    return {
        "summary": summary,
        "bad_postures": feedback,
        "neck_angles": neck_angles,
        "back_angles": back_angles
    }
