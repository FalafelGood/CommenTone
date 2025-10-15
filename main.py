"""
For a given YouTube channel, get the videos, get the comments for each video, 
run Vader analysis on the comments and then calculate some stats
"""

from channel_videos import get_channel_videos
from youtube_comments import get_video_comments
# from comment_analysis import sia
from comment_analysis import get_polarity_scores

def delete_old_logs():
  pass

def main(channel_id: str):
  videos = get_channel_videos(channel_id)
  for video_id in videos:
    # get all comments
    comments = get_video_comments(video_id)
    if comments:
      for comment in comments:
        print(comment['text'])
        scores = get_polarity_scores(comment['text'])
        print(scores)

main("@whitelist-media")