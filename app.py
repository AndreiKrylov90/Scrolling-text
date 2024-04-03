from flask import Flask, request, Response
import cv2
import numpy as np
import tempfile
import os

app = Flask(__name__)


@app.route('/generate')
def generate_video():
    text = request.args.get('text', 'Hello, World!')

    width, height = 100, 100
    fps = 25
    duration = 3
    text_speed = 2

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.avi')
    temp_filename = temp_file.name

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_filename, fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x_start = width
    text_y_start = height // 2 + text_size[1] // 2

    for frame_number in range(duration * fps):
        frame = np.zeros((height, width, 3), np.uint8)
        text_x = text_x_start - text_speed * frame_number
        if text_x + text_size[0] < 0:
            text_x = width
        cv2.putText(frame, text, (text_x, text_y_start), font, font_scale, (255, 255, 255), font_thickness)
        out.write(frame)

    out.release()

    with open(temp_filename, 'rb') as f:
        video_content = f.read()

    headers = {
        'Content-Disposition': f'attachment; filename=video.mp4'
    }

    return Response(video_content, mimetype='video/x-msvideo', headers=headers)


if __name__ == '__main__':
    app.run(debug=True)
