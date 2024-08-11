from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        try:
            # Create a YouTube object with the provided URL
            yt = YouTube(video_url)
            
            # Get the first progressive MP4 stream
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            
            if video_stream is None:
                return "No suitable video stream found."
            
            # Download the video
            video_stream.download()
            
            # Get the path to the downloaded video
            video_path = video_stream.default_filename
            
            # Send the file to the user
            return send_file(video_path, as_attachment=True)
        
        except Exception as e:
            # Handle exceptions and provide feedback
            return f"An error occurred: {str(e)}"
    
    # Render the HTML form for GET requests
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
