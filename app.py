from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(f"ytsearch:{query}", download=True)
                video_title = info_dict.get('title', 'download')
                
                return redirect(url_for('download', filename=f"{video_title}.mp3"))

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    return redirect(url_for('static', filename=f'downloads/{filename}'))

def progress_hook(d):
    if d['status'] == 'finished':
        print(f"\nDone downloading video: {d['filename']}")

if __name__ == "__main__":
    # Update to bind to all network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)
