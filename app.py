import os
from flask import Flask, render_template_string, request, send_from_directory
import subprocess

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBER_DUMP // تحميل يوتيوب حقيقي</title>
    <style>
        :root {
            --bg-dark: #05050a;
            --panel-bg: #0b0b16;
            --neon-cyan: #00f0ff;
            --neon-pink: #ff0055;
            --neon-yellow: #f4ee00;
            --text-main: #c0c0d0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Courier New', Courier, monospace; }
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: 
                linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
            background-size: 20px 20px;
            padding: 20px;
        }
        .terminal-container {
            width: 100%;
            max-width: 650px;
            background: var(--panel-bg);
            border: 2px solid var(--neon-cyan);
            box-shadow: 0 0 25px rgba(0, 240, 255, 0.25);
            padding: 30px;
            position: relative;
        }
        .terminal-container::before {
            content: "SYS_VER: 8.0.0 // RENDER_SERVER";
            position: absolute;
            top: -12px; right: 20px;
            background: var(--bg-dark);
            color: var(--neon-cyan);
            padding: 0 10px; font-size: 12px;
        }
        h1 { color: var(--neon-cyan); font-size: 20px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; color: var(--neon-pink); margin-bottom: 8px; font-size: 14px; text-transform: uppercase; }
        input[type="text"] {
            width: 100%; background: #020205; border: 1px solid var(--neon-cyan);
            color: #fff; padding: 12px; font-size: 16px; outline: none;
        }
        input[type="text"]:focus { border-color: var(--neon-pink); box-shadow: 0 0 10px rgba(255, 0, 85, 0.4); }
        button {
            background: transparent; border: 2px solid var(--neon-yellow);
            color: var(--neon-yellow); padding: 12px 20px; font-size: 16px;
            font-weight: bold; cursor: pointer; width: 100%; text-transform: uppercase;
            letter-spacing: 2px; transition: 0.3s;
        }
        button:hover { background: var(--neon-yellow); color: #000; box-shadow: 0 0 15px rgba(244, 238, 0, 0.5); }
        .status-box { margin-top: 20px; padding: 12px; border: 1px dashed; font-size: 14px; word-break: break-all; }
        .status-box.success { border-color: var(--neon-cyan); color: var(--neon-cyan); background: rgba(0, 240, 255, 0.05); }
        .status-box.error { border-color: var(--neon-pink); color: var(--neon-pink); background: rgba(255, 0, 85, 0.05); }
        .download-btn {
            display: block; text-align: center; margin-top: 15px;
            background: var(--neon-cyan); color: #000; padding: 14px;
            text-decoration: none; font-weight: bold; font-size: 16px;
            text-transform: uppercase; letter-spacing: 2px;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.4); transition: 0.3s;
        }
        .download-btn:hover { background: #fff; box-shadow: 0 0 25px #fff; }
    </style>
</head>
<body>
    <div class="terminal-container">
        <h1>> محطة_التحميل_السيبرانية [MAX_HD]</h1>
        <form method="POST">
            <div class="form-group">
                <label for="url">> أدخل رابط اليوتيوب المستهدف:</label>
                <input type="text" id="url" name="url" placeholder="https://www.youtube.com/watch?v=..." required>
            </div>
            <button type="submit">> تنفيذ السحب والدمج</button>
        </form>

        {% if message %}
            <div class="status-box {{ 'error' if error else 'success' }}">
                {{ message }}
            </div>
        {% endif %}

        {% if filename %}
            <a href="/download/{{ filename }}" class="download-btn" download>> تحميل الفيديو للجهاز (MP4) </a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    filename = ''
    error = False

    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            try:
                output_template = os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s')
                
                # جلب اسم الملف المتوقع
                cmd_filename = ["yt-dlp", "--print", "filename", "-f", "bv*+ba/b", url]
                target_filename = subprocess.check_output(cmd_filename, text=True).strip()
                
                if target_filename:
                    base_id = os.path.splitext(os.path.basename(target_filename))[0]
                    final_filename = f"{base_id}.mp4"
                    final_path = os.path.join(DOWNLOAD_DIR, final_filename)
                    
                    # أمر التحميل والدمج بأعلى جودة
                    download_command = [
                        "yt-dlp",
                        "-f", "bv*+ba/b",
                        "--merge-output-format", "mp4",
                        "-o", output_template,
                        url
                    ]
                    
                    subprocess.run(download_command, check=True)
                    
                    if os.path.exists(final_path):
                        filename = final_filename
                        message = "[ تم اكتمال الدمج والسحب بنجاح: أعلى جودة متاحة ]"
                    else:
                        error = True
                        message = "[ خطأ: فشل حفظ الملف الناتج على السيرفر ]"
                else:
                    error = True
                    message = "[ خطأ: تعذر قراءة بيانات الفيديو ]"
            except Exception as e:
                error = True
                message = f"[ خطأ تقني: {str(e)} ]"
        else:
            error = True
            message = "[ خطأ: يرجى إدخال رابط صالح ]"

    return render_template_string(HTML_TEMPLATE, message=message, filename=filename, error=error)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
