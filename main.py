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
from vaderscores import VaderScores
from setup_logging import setup_logging

def rate_channel_by_comments(channel_id: str, max_comments_per_vid = 100, max_vids = 50):
  """
  First, see if Channels / ChannelName exists. If it doesn't, create the appropriate folder
  In this folder, we'll dump all of the comments together with their scores
  """
  logger = logging.getLogger(__name__)
  logger.info(f"Starting analysis for channel: {channel_id}")
  videos = get_channel_videos(channel_id)
  logger.info(f"Found {len(videos)} videos for channel {channel_id}")

  scores = VaderScores()

  # Limit to max_vids videos
  for video_id in videos[:max_vids]:
    comments = get_video_comments(video_id)
    if comments:
      for comment in comments:
      # for comment in comments[:max_comments_per_vid]:
        score = get_polarity_scores(comment['text'])
        like_count = comment['like_count']
        scores.add_score(score, like_count)

  weighted_average_scores = scores.weighted_average_scores()
  # average_scores = scores.average_scores()
  # score_varience = scores.score_variances()
  # print(average_scores)
  # print(score_varience)
  print(weighted_average_scores)
  print(f"Kindness: {scores.kindness()}")
  print(f"Volatility: {scores.volatility()}")


if __name__ == '__main__':
  logger = setup_logging()
  rate_channel_by_comments("@BishopBarron", max_vids=3)
  