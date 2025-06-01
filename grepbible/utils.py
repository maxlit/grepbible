from pathlib import Path

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
        # Split the line into path and content
        file_path, verse_num, text = grep_line.rsplit(':', 2)
        
        # Extract book and chapter from path
        path = Path(file_path)
        book = path.parent.name
        chapter = path.stem  # removes .txt extension
        
        return f"{book} {chapter}:{verse_num} {text}"
    except ValueError:
        raise ValueError(f"Invalid grep format: {grep_line}")
