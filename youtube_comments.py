#!/usr/bin/env python3
"""
YouTube Comments Fetcher

A Python script that uses the official YouTube Data API v3 to fetch all comments
from a YouTube video by its video ID.

Requirements:
- Google API key
- google-api-python-client library
- requests library

Usage:
    python youtube_comments.py --video-id VIDEO_ID --api-key YOUR_API_KEY
"""

import json
import sys
import time
import logging
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# import os

# Module-level logger
logger = logging.getLogger(__name__)

class YouTubeCommentsFetcher:
    """Fetches comments from YouTube videos using the YouTube Data API v3."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the YouTubeCommentsFetcher.
        
        Args:
            api_key: YouTube Data API key
        """
        self.api_key = api_key
        self.youtube = None # Discovery document
        self._initialize_api()
    
    def _initialize_api(self):
        """Initialize the YouTube API client."""
        try:
            if self.api_key:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            else:
                raise ValueError("api_key must be provided")
                
        except Exception as e:
            logger.error(f" Error initializing YouTube API: {e}")
            sys.exit(1)
    
    def get_video_info(self, video_id: str) -> Dict:
        """
        Get basic information about the video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing video information
        """
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                return None
            
            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'channel': video['snippet']['channelTitle'],
                'view_count': video['statistics'].get('viewCount', 0),
                'like_count': video['statistics'].get('likeCount', 0),
                'comment_count': video['statistics'].get('commentCount', 0)
            }
        except HttpError as e:
            logger.error(f"Error fetching video info: {e}")
            return None
    
    def get_all_comments(self, video_id: str, max_results: int = 100) -> List[Dict]:
        """
        Fetch all comments from a YouTube video.
        
        Args:
            video_id: YouTube video ID
            max_results: Maximum number of comments to fetch per request (max 100)
            
        Returns:
            List of comment dictionaries
        """
        all_comments = []
        next_page_token = None
        
        logger.info(f"Fetching comments for video ID: {video_id}")
        
        try:
            while True:
                # Get top-level comments
                request = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=min(max_results, 100),
                    pageToken=next_page_token,
                    order='time'  # You can change this to 'relevance' or 'time'
                )
                
                response = request.execute()
                
                for item in response['items']:
                    comment = self._extract_comment_data(item)
                    all_comments.append(comment)
                    
                    # Get replies to this comment
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            reply_data = self._extract_reply_data(reply, comment['id'])
                            all_comments.append(reply_data)
                
                # Check if there are more pages
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                
                # Rate limiting - YouTube API has quotas
                time.sleep(0.1)
                
        except HttpError as e:
            if e.resp.status == 403:
                logger.error("API quota exceeded or access denied. Please check your API key and quota.")
            elif e.resp.status == 404:
                logger.error("Video not found or comments disabled.")
            else:
                logger.error(f"Error fetching comments: {e}")
            return all_comments
        
        logger.info(f"Successfully fetched {len(all_comments)} comments")
        return all_comments
    
    def _extract_comment_data(self, item: Dict) -> Dict:
        """Extract comment data from API response."""
        snippet = item['snippet']['topLevelComment']['snippet']
        return {
            'id': item['snippet']['topLevelComment']['id'],
            'parent_id': None,
            'author': snippet['authorDisplayName'],
            'author_channel_id': snippet.get('authorChannelId', {}).get('value'),
            'text': snippet['textDisplay'],
            'like_count': snippet['likeCount'],
            'published_at': snippet['publishedAt'],
            'updated_at': snippet['updatedAt'],
            'is_reply': False
        }
    
    def _extract_reply_data(self, reply: Dict, parent_id: str) -> Dict:
        """Extract reply data from API response."""
        snippet = reply['snippet']
        return {
            'id': reply['id'],
            'parent_id': parent_id,
            'author': snippet['authorDisplayName'],
            'author_channel_id': snippet.get('authorChannelId', {}).get('value'),
            'text': snippet['textDisplay'],
            'like_count': snippet['likeCount'],
            'published_at': snippet['publishedAt'],
            'updated_at': snippet['updatedAt'],
            'is_reply': True
        }
    
    def save_comments_to_file(self, comments: List[Dict], filename: str):
        """
        Save comments to a JSON file.
        
        Args:
            comments: List of comment dictionaries
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(comments, f, indent=2, ensure_ascii=False)
            logger.info(f"Comments saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving comments: {e}")


def get_video_comments(video_id: str, max_results: Optional[int] = 100):


    try:
        from config import YOUTUBE_API_KEY
    except ImportError:
        print("YOUTUBE_API_KEY not found in config.py", ImportError)
        print("Have you configured your API key? Follow the instructions in config-template.py for more info")
        sys.exit(1)
    
    # Initialize the fetcher
    fetcher = YouTubeCommentsFetcher(
        api_key=YOUTUBE_API_KEY
    )

    # Fetch all comments
    comments = fetcher.get_all_comments(video_id, max_results)
    if comments:
        return comments
    else:
        print("WARNING: No comments were found, or some other error occoured.")



if __name__ == '__main__':
    """
    A simple unit test: This should get the comments from one of my videos and log them in a seperate file.
    """
    from setup_logging import setup_logging
    logger = setup_logging()
    logger.info(" Running unit test for youtube_comments.py")
    comments = get_video_comments(video_id="17AhCNBljME")
    for comment in comments:
        logger.debug(comment['text'])

