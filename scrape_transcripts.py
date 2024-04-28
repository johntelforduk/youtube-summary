from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import time
import datetime
from urllib.parse import quote


def get_transcript(this_id: str) -> str:
    transcript_list = YouTubeTranscriptApi.get_transcript(this_id)
    full_text = ''
    for line in transcript_list:
        if full_text != '':
            full_text += '\n'
        full_text += line['text']
    return full_text


def create_filename(this_title: str) -> str:
    return quote(this_title.replace(' ', '_')) + '.txt'


with open('ids_full.txt', 'r') as file:
    ids = file.read()

for video_id in ids.split('\n'):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        title = yt.title
        description = yt.description
        publish_date = yt.publish_date.strftime('%d %B %Y')

        filename = create_filename(title)
        transcript = get_transcript(video_id)

        print(f'video_id={video_id}, title={title}, publish_date={publish_date}, filename={filename}, len(transcript)={len(transcript)}')

        f = open(f'./transcripts/{filename}', 'w')
        f.write(f'Title: {title}\n')
        f.write(f'Published: {publish_date}\n')
        f.write('\n---\n\n')
        f.write(transcript)
        f.close()

    except:
        print(f'Could not create YouTube object, video_id={video_id}')

    time.sleep(1)
