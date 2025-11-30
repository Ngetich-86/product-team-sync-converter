"""
Markdown parser for converting meeting notes to Google Docs formatting.
"""

import re

def parse_markdown_line(line):
    """
    Parse a single markdown line and return its type, content, and metadata.
    
    Returns:
        dict: {
            'type': str,  # heading, bullet, checkbox, text, separator, footer
            'content': str,
            'level': int, # 0-based indentation level or heading level
            'original': str
        }
    """
    original_line = line
    line = line.rstrip()
    
    if not line:
        return {'type': 'empty', 'content': '', 'level': 0, 'original': original_line}
        
    # Calculate indentation (2 spaces = 1 level)
    indent_match = re.match(r'^(\s*)', line)
    indent_spaces = len(indent_match.group(1))
    level = indent_spaces // 2
    
    content = line.strip()
    
    # Separator
    if content == '---':
        return {'type': 'separator', 'content': '', 'level': 0, 'original': original_line}
        
    # Headings
    if content.startswith('#'):
        heading_match = re.match(r'^(#+)\s+(.+)$', content)
        if heading_match:
            h_level = len(heading_match.group(1))
            return {
                'type': 'heading',
                'content': heading_match.group(2),
                'level': h_level,
                'original': original_line
            }
            
    # Checkboxes
    if content.startswith('- [ ] ') or content.startswith('* [ ] '):
        return {
            'type': 'checkbox',
            'content': content[6:],
            'level': level,
            'original': original_line
        }
        
    # Bullets
    if content.startswith('- ') or content.startswith('* '):
        return {
            'type': 'bullet',
            'content': content[2:],
            'level': level,
            'original': original_line
        }
        
    # Footer detection (heuristic)
    if content.startswith('Meeting recorded by:') or content.startswith('Duration:'):
        return {
            'type': 'footer',
            'content': content,
            'level': 0,
            'original': original_line
        }

    return {'type': 'text', 'content': content, 'level': level, 'original': original_line}
