import re

class GoogleDocBuilder:
    """
    Builds a list of Google Docs API requests to format a document based on parsed markdown.
    """
    def __init__(self):
        self.requests = []
        self.current_index = 1
        
    def build_requests(self, parsed_lines):
        """
        Convert parsed markdown lines into Google Docs API requests.
        """
        self.requests = []
        self.current_index = 1
        
        for line in parsed_lines:
            self._process_line(line)
            
        return self.requests
    
    def _process_line(self, line):
        line_type = line['type']
        content = line['content']
        level = line['level']
        
        if line_type == 'empty':
            self._insert_text("\n")
            return
            
        if line_type == 'separator':
            # Insert a horizontal rule or just a divider line
            self._insert_text("--------------------------------------------------\n")
            return

        # Prepare text to insert (add newline)
        text_to_insert = content + "\n"
        start_index = self.current_index
        self._insert_text(text_to_insert)
        end_index = self.current_index # _insert_text updates current_index
        
        # Apply Paragraph Styles
        if line_type == 'heading':
            style = f'HEADING_{level}'
            self._update_paragraph_style(start_index, end_index, style)
            
        elif line_type == 'bullet':
            self._create_bullet(start_index, end_index, 'BULLET_DISC_CIRCLE_SQUARE')
            self._handle_indentation(start_index, end_index, level)
            
        elif line_type == 'checkbox':
            self._create_bullet(start_index, end_index, 'BULLET_CHECKBOX')
            self._handle_indentation(start_index, end_index, level)
            
        elif line_type == 'footer':
            self._style_footer(start_index, end_index)
            
        # Apply Text Styles (Mentions, Bold, etc.)
        self._style_mentions(content, start_index)
        
    def _insert_text(self, text):
        self.requests.append({
            'insertText': {
                'location': {'index': self.current_index},
                'text': text
            }
        })
        self.current_index += len(text)
        
    def _update_paragraph_style(self, start, end, named_style):
        self.requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': start,
                    'endIndex': end
                },
                'paragraphStyle': {
                    'namedStyleType': named_style
                },
                'fields': 'namedStyleType'
            }
        })
        
    def _create_bullet(self, start, end, preset):
        self.requests.append({
            'createParagraphBullets': {
                'range': {
                    'startIndex': start,
                    'endIndex': end
                },
                'bulletPreset': preset
            }
        })

    def _handle_indentation(self, start, end, level):
        if level > 0:
            indent_start = 36 * (level + 1)
            self.requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'paragraphStyle': {
                        'indentStart': {'magnitude': indent_start, 'unit': 'PT'},
                        'indentFirstLine': {'magnitude': indent_start - 18, 'unit': 'PT'}
                    },
                    'fields': 'indentStart,indentFirstLine'
                }
            })

    def _style_mentions(self, content, start_index):
        # Find all mentions @name
        for match in re.finditer(r'@(\w+)', content):
            mention_start = start_index + match.start()
            mention_end = start_index + match.end()
            
            self.requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': mention_start,
                        'endIndex': mention_end
                    },
                    'textStyle': {
                        'bold': True,
                        'foregroundColor': {
                            'color': {'rgbColor': {'red': 0.2, 'green': 0.5, 'blue': 0.8}}
                        }
                    },
                    'fields': 'bold,foregroundColor'
                }
            })

    def _style_footer(self, start, end):
        self.requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': start,
                    'endIndex': end
                },
                'textStyle': {
                    'italic': True,
                    'foregroundColor': {
                        'color': {'rgbColor': {'red': 0.5, 'green': 0.5, 'blue': 0.5}}
                    },
                    'fontSize': {'magnitude': 10, 'unit': 'PT'}
                },
                'fields': 'italic,foregroundColor,fontSize'
            }
        })
