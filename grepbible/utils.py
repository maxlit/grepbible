from pathlib import Path
import re

def grep_to_citation(grep_line):
    """Convert grep-style Bible reference to citation format.
    
    Args:
        grep_line (str): Line in format "path/to/Book/Chapter.txt:Verse:Text"
    
    Returns:
        str: Formatted citation "Book Chapter:Verse Text"
        
    Example:
        >>> grep_to_citation("/path/to/Daniel/10.txt:3:I ate no pleasant bread")
        "Daniel 10:3 I ate no pleasant bread"
    """
    try:
        # Use regex to match the pattern: path/to/Book/Chapter.txt:Verse:Text
        pattern = r'^(.+?)/([^/]+)/(\d+)\.txt:(\d+):(.+)$'
        match = re.match(pattern, grep_line)
        if not match:
            raise ValueError(f"Invalid grep format: {grep_line}")
        
        # Extract components
        _, book, chapter, verse_num, text = match.groups()
        
        return f"{book} {chapter}:{verse_num} {text}"
    except Exception as e:
        raise ValueError(f"Invalid grep format: {grep_line}") from e
