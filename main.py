from flask import Flask, redirect, url_for, render_template, request, send_from_directory
import os
import threading
import pygame

app = Flask(__name__)
app.sercret_key = '123123'

# Thư mục chứa các file nhạc
MUSIC_DIR = "D:\code\CNPM\music"

# Biến lưu trạng thái phát nhạc (True là đang phát, False là dừng)
is_playing = False

# Biến đăng nhập
login = True
# Biến lưu trạng thái bài hát đang được phát
current_song = None

# Khởi tạo Pygame
pygame.init()

def play_music(filename):
    global is_playing
    # Xây dựng đường dẫn đến tập tin âm thanh
    music_path = os.path.join(MUSIC_DIR, filename)
    
    # Kiểm tra xem tập tin âm thanh tồn tại không
    if not os.path.exists(music_path):
        print(f"Không tìm thấy tập tin âm thanh: {filename}")
        return
    
    # Phát nhạc
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if not is_playing:
            pygame.mixer.music.stop()
            break


def extract_song_info(filename):
    # Kiểm tra xem tên tập tin có đúng định dạng không
    if '-' not in filename or '.mp3' not in filename:
        return None, None
    
    # Tách tên tập tin bằng dấu "-"
    parts = filename.split('-')
    
    # Kiểm tra xem có đủ phần trong tên tập tin không
    if len(parts) != 2:
        return None, None
    
    # Phần đầu tiên là tên bài hát
    song_name = parts[0].strip()
    
    # Phần thứ hai là tên tác giả, loại bỏ phần mở rộng .mp3
    artist_name = parts[1].replace('.mp3', '').strip()
    
    return song_name, artist_name

# Route mặc định: hiển thị danh sách các bài hát
@app.route('/')
def index():
    # Get the list of music files
    music_files = os.listdir(MUSIC_DIR)
    
    # Extract song info for each music file
    songs_info = []
    for file in music_files:
        song_name, artist_name = extract_song_info(file)
        songs_info.append({'song_name': song_name, 'artist_name': artist_name})
    
    return render_template('index.html', songs_info=songs_info, is_playing=is_playing, current_song=current_song)

# Route để phát nhạc
@app.route('/play/<filename>')
def start_playing(filename):
    global is_playing
    global current_song
    is_playing = True
    current_song = filename
    print("Current song:", current_song)  # Kiểm tra giá trị của current_song
    threading.Thread(target=play_music, args=(filename,)).start()
    return redirect(url_for('index'))

# Route để dừng nhạc và quay về danh sách bài hát
@app.route('/stop')
def stop_playing():
    global is_playing
    is_playing = False
    return redirect(url_for('index'))

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
    app.run(host='0.0.0.0', port=5000, debug=True)
