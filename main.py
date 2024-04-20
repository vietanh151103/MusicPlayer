from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Thư mục chứa các file nhạc
MUSIC_DIR = "D:\code\CNPM\music"#chuyển path theo thư mục lưu music

# Route mặc định: hiển thị danh sách các bài hát
@app.route('/')
def index():
    songs = os.listdir(MUSIC_DIR)
    return render_template('index.html', songs=songs)

# Route để phát nhạc
@app.route('/play/<song>')
def play(song):
    return f'Phát nhạc: {song}'

# Route để tìm kiếm bài hát
@app.route('/search')
def search():
    query = request.args.get('query')
    songs = os.listdir(MUSIC_DIR)
    results = [song for song in songs if query.lower() in song.lower()]
    return render_template('search_results.html', query=query, results=results)

# Route để tải xuống bài hát
@app.route('/download/<song>')
def download(song):
    return send_from_directory(MUSIC_DIR, song, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
