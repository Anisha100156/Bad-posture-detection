from flask import Blueprint, request, jsonify
import tempfile
from app.services.posture_analyzer import analyze_posture
posture_bp = Blueprint('posture_bp', __name__)
@posture_bp.route('/analyze', methods=['POST'])
def analyze():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400
    video_file = request.files['video']
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp:
        video_path = temp.name
        video_file.save(video_path)
    result = analyze_posture(video_path)
    feedback = result.get("bad_postures", [])
    neck_angles = result.get("neck_angles", [])
    back_angles = result.get("back_angles", [])
    total_frames = len(feedback)
    good_frames = sum(
        1 for msg in feedback 
        if 'Perfect neck posture' in msg and 
           'Good back posture' in msg and 
           'Knee within safe range' in msg
    )
    if total_frames == 0:
        summary = "No frames were processed."
        advice = "No posture could be detected."
        avg_neck = 0
        avg_back = 0
    elif good_frames == total_frames:
        summary = "🟢 Perfect posture throughout the video!"
        advice = "Keep it up! You're sitting straight!"
        avg_neck = sum(neck_angles) / len(neck_angles)
        avg_back = sum(back_angles) / len(back_angles)
    else:
        avg_neck = sum(neck_angles) / len(neck_angles) if neck_angles else 0
        avg_back = sum(back_angles) / len(back_angles) if back_angles else 0
        summary = f"🧍 Posture needs improvement. Only {good_frames}/{total_frames} frames were good."
        advice = (
            f"Your average neck tilt was {avg_neck:.1f}°. Tilt your neck backward by approx {avg_neck:.1f}° to align straight. "
            f"Your average back angle was {avg_back:.1f}°. Try to keep it above 150° for a straight back."
        )
    return jsonify({
        'summary': summary,
        'advice': advice,
        'bad_postures': feedback,
        'avg_neck_angle': round(avg_neck, 2),
        'avg_back_angle': round(avg_back, 2),
        'total_frames': total_frames,
        'good_frames': good_frames
    })
