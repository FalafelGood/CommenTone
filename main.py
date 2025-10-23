"""
For a given YouTube channel, get the videos, get the comments for each video, 
run Vader analysis on the comments and then calculate some stats
"""

import logging
import sys
from datetime import datetime
from channel_videos import get_channel_videos
from youtube_comments import get_video_comments
from comment_analysis import get_polarity_scores
from setup_logging import setup_logging

def rate_channel_by_comments(channel_id: str):
  """
  First, see if Channels / ChannelName exists. If it doesn't, create the appropriate folder
  In this folder, we'll dump all of the comments together with their scores
  """
  logger = logging.getLogger(__name__)
  logger.info(f"Starting analysis for channel: {channel_id}")
  videos = get_channel_videos(channel_id)
  logger.info(f"Found {len(videos)} videos for channel {channel_id}")

  for video_id in videos:
    comments = get_video_comments(video_id)
    if comments:
      for comment in comments:
        scores = get_polarity_scores(comment['text'])
        print("\"" + comment['text'] + "\"" + ' ' + str(scores))

if __name__ == '__main__':
  logger = setup_logging()
  rate_channel_by_comments("@whitelist-media")
  # # logger.info(f"Starting analysis for channel: {channel_id}")
  # videos = get_channel_videos("@whitelist-media")
  # get_video_comments("17AhCNBljME", output_file="my-vid.txt")
  