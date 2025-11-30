"""Echo Hearts - Main application entry point."""

import logging
from src.ui.interface import launch_interface

# Configure logging to show DEBUG messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)

if __name__ == "__main__":
    launch_interface()
