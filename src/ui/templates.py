"""HTML/Markdown templates for Echo Hearts UI."""

LANDING_PAGE = """
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 20px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
    <h1 style="color: white; font-size: 4em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); letter-spacing: 0.1em;">
        💕 ECHO HEARTS
    </h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.4em; font-style: italic; margin-top: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
        A Mystery Escape Room - Investigate, Collaborate, and Escape the Unknown
    </p>
</div>

---

<div style="text-align: center; padding: 20px;">

## About The Game

You wake up in a strange facility with no memory of how you got there.

Someone else is with you. She seems just as confused as you are.

The doors are locked. You need to work together to escape.

**Navigate 5 rooms. Solve puzzles. Uncover the truth.**

*Simple, right?*

</div>
"""


def get_landing_page() -> str:
    """Get the landing page HTML.

    Returns:
        Landing page HTML/Markdown string
    """
    return LANDING_PAGE
