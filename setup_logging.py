import logging
import sys
from datetime import datetime

def setup_logging():
  """Configure logging for the CommenTone application"""
  # Create log directory if it doesn't exist.
  import os
  os.makedirs('logs', exist_ok=True)

  timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
  log_filename = f'logs/commentone_{timestamp}.log'

  logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
      logging.FileHandler(log_filename, encoding='utf-8'),
      # Uncomment to also log to console
      logging.StreamHandler(sys.stdout) 
    ]
  )

  # Supress verbose logging from third-party libraries:
  logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.WARNING)
  logging.getLogger('googleapiclient.discovery').setLevel(logging.WARNING)
  logging.getLogger('urllib3').setLevel(logging.WARNING)

  # Create instance of module-level logger
  logger = logging.getLogger(__name__)
  logger.info(f"Logger initialized. Log file: {log_filename}")
  return logger
