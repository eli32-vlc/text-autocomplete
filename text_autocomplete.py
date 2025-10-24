"""
Text editor with AI-powered autocomplete.
A TUI application similar to nano with GitHub Copilot-style word completion.
"""
import curses
import time
import os
from typing import List, Optional, Tuple
from config_manager import Config
from ai_completer import AICompleter


class TextEditor:
    """Main text editor class with AI autocomplete."""
    
    def __init__(self, stdscr, filename: Optional[str] = None):
        """Initialize text editor.
        
        Args:
            stdscr: Curses standard screen object
            filename: Optional filename to load
        """
        self.stdscr = stdscr
        self.filename = filename
        self.config = Config()
        self.ai_completer = AICompleter(self.config)
        
        # Text buffer (list of lines)
        self.lines: List[str] = [""]
        self.cursor_y = 0
        self.cursor_x = 0
        self.offset_y = 0  # Scroll offset
        
        # AI completion state
        self.suggestion: str = ""
        self.suggestion_match_pos = 0  # How many chars of suggestion match
        self.last_input_time = 0
        self.ai_enabled = True
        self.requesting_completion = False
        
        # Display state
        self.modified = False
        self.status_message = ""
        self.status_message_time = 0
        
        # Screen dimensions
        self.height, self.width = stdscr.getmaxyx()
        self.text_height = self.height - 3  # Leave room for status and help
        
        # Colors
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Status bar
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Ghost text
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Help text
        
        # Load file if specified
        if filename and os.path.exists(filename):
            self.load_file(filename)
        
        # Setup non-blocking input
        stdscr.nodelay(True)
        stdscr.keypad(True)
    
    def load_file(self, filename: str):
        """Load file into buffer.
        
        Args:
            filename: Path to file to load
        """
        try:
            with open(filename, 'r') as f:
                content = f.read()
                if content:
                    self.lines = content.split('\n')
                else:
                    self.lines = [""]
                self.filename = filename
                self.modified = False
                self.set_status(f"Loaded {filename}")
        except IOError as e:
            self.set_status(f"Error loading file: {e}")
    
    def save_file(self, filename: Optional[str] = None):
        """Save buffer to file.
        
        Args:
            filename: Path to save to (uses self.filename if None)
        """
        if filename:
            self.filename = filename
        
        if not self.filename:
            self.set_status("No filename specified")
            return
        
        try:
            with open(self.filename, 'w') as f:
                f.write('\n'.join(self.lines))
            self.modified = False
            self.set_status(f"Saved to {self.filename}")
        except IOError as e:
            self.set_status(f"Error saving file: {e}")
    
    def set_status(self, message: str):
        """Set status message.
        
        Args:
            message: Status message to display
        """
        self.status_message = message
        self.status_message_time = time.time()
    
    def get_current_line(self) -> str:
        """Get the current line text.
        
        Returns:
            Current line text
        """
        return self.lines[self.cursor_y] if self.cursor_y < len(self.lines) else ""
    
    def get_context_before_cursor(self, max_chars: int = 500) -> str:
        """Get text context before cursor for AI completion.
        
        Args:
            max_chars: Maximum characters to include
            
        Returns:
            Context string
        """
        # Get all text up to cursor position
        context_lines = []
        
        # Add previous lines
        for i in range(max(0, self.cursor_y - 10), self.cursor_y):
            context_lines.append(self.lines[i])
        
        # Add current line up to cursor
        current_line = self.get_current_line()
        context_lines.append(current_line[:self.cursor_x])
        
        context = '\n'.join(context_lines)
        
        # Trim to max_chars
        if len(context) > max_chars:
            context = context[-max_chars:]
        
        return context
    
    def request_ai_completion(self):
        """Request AI completion based on current context."""
        if not self.ai_enabled or not self.ai_completer.is_available():
            return
        
        if self.requesting_completion:
            return
        
        context = self.get_context_before_cursor()
        if not context.strip():
            return
        
        # Non-blocking request (in a real implementation, this would be async)
        # For simplicity, we'll do it synchronously with short timeout
        self.requesting_completion = True
        completion = self.ai_completer.get_completion(context)
        self.requesting_completion = False
        
        if completion:
            self.suggestion = completion
            self.suggestion_match_pos = 0
    
    def check_suggestion_match(self, char: str):
        """Check if typed character matches suggestion.
        
        Args:
            char: Character that was typed
        """
        if not self.suggestion:
            return
        
        if self.suggestion_match_pos < len(self.suggestion):
            if self.suggestion[self.suggestion_match_pos] == char:
                self.suggestion_match_pos += 1
            else:
                # Mismatch - clear suggestion
                self.suggestion = ""
                self.suggestion_match_pos = 0
        else:
            # Already matched all of suggestion
            self.suggestion = ""
            self.suggestion_match_pos = 0
    
    def accept_suggestion(self):
        """Accept the current AI suggestion."""
        if not self.suggestion:
            return
        
        # Get remaining suggestion (after matched portion)
        remaining = self.suggestion[self.suggestion_match_pos:]
        if not remaining:
            self.suggestion = ""
            return
        
        # Insert remaining suggestion at cursor
        current_line = self.get_current_line()
        new_line = current_line[:self.cursor_x] + remaining + current_line[self.cursor_x:]
        self.lines[self.cursor_y] = new_line
        self.cursor_x += len(remaining)
        self.modified = True
        
        # Clear suggestion
        self.suggestion = ""
        self.suggestion_match_pos = 0
    
    def insert_char(self, char: str):
        """Insert character at cursor position.
        
        Args:
            char: Character to insert
        """
        current_line = self.get_current_line()
        new_line = current_line[:self.cursor_x] + char + current_line[self.cursor_x:]
        self.lines[self.cursor_y] = new_line
        self.cursor_x += 1
        self.modified = True
        
        # Check if char matches suggestion
        self.check_suggestion_match(char)
        
        # Reset timer for AI request
        self.last_input_time = time.time()
    
    def delete_char(self):
        """Delete character before cursor (backspace)."""
        if self.cursor_x > 0:
            current_line = self.get_current_line()
            new_line = current_line[:self.cursor_x - 1] + current_line[self.cursor_x:]
            self.lines[self.cursor_y] = new_line
            self.cursor_x -= 1
            self.modified = True
            
            # Clear suggestion on delete
            self.suggestion = ""
            self.suggestion_match_pos = 0
            self.last_input_time = time.time()
        elif self.cursor_y > 0:
            # Join with previous line
            previous_line = self.lines[self.cursor_y - 1]
            current_line = self.get_current_line()
            self.lines[self.cursor_y - 1] = previous_line + current_line
            del self.lines[self.cursor_y]
            self.cursor_y -= 1
            self.cursor_x = len(previous_line)
            self.modified = True
            self.suggestion = ""
            self.suggestion_match_pos = 0
            self.last_input_time = time.time()
    
    def insert_newline(self):
        """Insert newline at cursor position."""
        current_line = self.get_current_line()
        before = current_line[:self.cursor_x]
        after = current_line[self.cursor_x:]
        
        self.lines[self.cursor_y] = before
        self.lines.insert(self.cursor_y + 1, after)
        self.cursor_y += 1
        self.cursor_x = 0
        self.modified = True
        
        # Clear suggestion
        self.suggestion = ""
        self.suggestion_match_pos = 0
        self.last_input_time = time.time()
    
    def move_cursor(self, dy: int, dx: int):
        """Move cursor by delta.
        
        Args:
            dy: Vertical movement
            dx: Horizontal movement
        """
        # Clear suggestion on cursor movement (except right arrow which accepts)
        if dy != 0 or (dx < 0):
            self.suggestion = ""
            self.suggestion_match_pos = 0
        
        # Vertical movement
        new_y = max(0, min(len(self.lines) - 1, self.cursor_y + dy))
        if new_y != self.cursor_y:
            self.cursor_y = new_y
            # Adjust cursor_x to fit new line
            line_len = len(self.get_current_line())
            self.cursor_x = min(self.cursor_x, line_len)
        
        # Horizontal movement
        if dx != 0:
            line_len = len(self.get_current_line())
            self.cursor_x = max(0, min(line_len, self.cursor_x + dx))
    
    def draw(self):
        """Draw the editor interface."""
        self.stdscr.clear()
        
        # Update scroll offset to keep cursor visible
        if self.cursor_y < self.offset_y:
            self.offset_y = self.cursor_y
        elif self.cursor_y >= self.offset_y + self.text_height:
            self.offset_y = self.cursor_y - self.text_height + 1
        
        # Draw text lines
        for i in range(self.text_height):
            line_idx = i + self.offset_y
            if line_idx < len(self.lines):
                line = self.lines[line_idx]
                
                # Draw the main text
                if len(line) <= self.width - 1:
                    self.stdscr.addstr(i, 0, line)
                else:
                    self.stdscr.addstr(i, 0, line[:self.width - 1])
                
                # Draw suggestion (ghost text) if on cursor line
                if line_idx == self.cursor_y and self.suggestion:
                    ghost_x = self.cursor_x
                    if ghost_x < self.width - 1:
                        remaining = self.suggestion[self.suggestion_match_pos:]
                        max_len = min(len(remaining), self.width - 1 - ghost_x)
                        if max_len > 0:
                            try:
                                self.stdscr.addstr(
                                    i, ghost_x, 
                                    remaining[:max_len], 
                                    curses.color_pair(2) | curses.A_DIM
                                )
                            except curses.error:
                                pass  # Ignore drawing errors at screen edge
        
        # Draw status bar
        status_y = self.height - 3
        status_text = f" {self.filename or '[No Name]'} "
        if self.modified:
            status_text += "[Modified] "
        status_text += f"| Line {self.cursor_y + 1}/{len(self.lines)} Col {self.cursor_x + 1}"
        if not self.ai_completer.is_available():
            status_text += " | AI: Not configured"
        elif not self.ai_enabled:
            status_text += " | AI: Disabled"
        else:
            status_text += " | AI: Enabled"
        
        # Pad status text
        status_text = status_text.ljust(self.width - 1)
        try:
            self.stdscr.addstr(status_y, 0, status_text, curses.color_pair(1))
        except curses.error:
            pass
        
        # Draw status message if recent
        if time.time() - self.status_message_time < 3:
            msg_y = self.height - 2
            msg = self.status_message[:self.width - 1]
            try:
                self.stdscr.addstr(msg_y, 0, msg, curses.color_pair(3))
            except curses.error:
                pass
        
        # Draw help line
        help_y = self.height - 1
        help_text = "^S Save | ^O Open | ^X Exit | ^G Toggle AI | Tab/→ Accept"
        help_text = help_text[:self.width - 1]
        try:
            self.stdscr.addstr(help_y, 0, help_text, curses.color_pair(3))
        except curses.error:
            pass
        
        # Position cursor
        screen_y = self.cursor_y - self.offset_y
        if 0 <= screen_y < self.text_height:
            try:
                self.stdscr.move(screen_y, self.cursor_x)
            except curses.error:
                pass
        
        self.stdscr.refresh()
    
    def handle_input(self):
        """Handle keyboard input."""
        try:
            key = self.stdscr.getch()
            
            if key == -1:  # No input
                # Check if we should request AI completion
                if self.ai_enabled and not self.suggestion and not self.requesting_completion:
                    current_time = time.time()
                    delay_seconds = self.config.pause_delay_ms / 1000.0
                    if current_time - self.last_input_time > delay_seconds:
                        if self.last_input_time > 0:  # Only if user has typed something
                            self.request_ai_completion()
                return True
            
            # Ctrl+X - Exit
            if key == 24:  # Ctrl+X
                if self.modified:
                    self.set_status("Save changes? (^S to save, ^X again to exit)")
                    return True
                return False
            
            # Ctrl+S - Save
            elif key == 19:  # Ctrl+S
                self.save_file()
            
            # Ctrl+O - Open
            elif key == 15:  # Ctrl+O
                self.set_status("Open: (enter filename then press Enter)")
                # TODO: Implement filename prompt
            
            # Ctrl+G - Toggle AI
            elif key == 7:  # Ctrl+G
                self.ai_enabled = not self.ai_enabled
                status = "enabled" if self.ai_enabled else "disabled"
                self.set_status(f"AI autocomplete {status}")
                if not self.ai_enabled:
                    self.suggestion = ""
            
            # Tab or Right Arrow - Accept suggestion
            elif key == 9 or key == curses.KEY_RIGHT:  # Tab or Right
                if self.suggestion:
                    self.accept_suggestion()
                elif key == curses.KEY_RIGHT:
                    self.move_cursor(0, 1)
            
            # Arrow keys
            elif key == curses.KEY_UP:
                self.move_cursor(-1, 0)
            elif key == curses.KEY_DOWN:
                self.move_cursor(1, 0)
            elif key == curses.KEY_LEFT:
                self.move_cursor(0, -1)
            
            # Backspace
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                self.delete_char()
            
            # Enter
            elif key in (curses.KEY_ENTER, 10, 13):
                self.insert_newline()
            
            # Regular character
            elif 32 <= key <= 126:
                self.insert_char(chr(key))
            
            return True
            
        except KeyboardInterrupt:
            return False
    
    def run(self):
        """Main editor loop."""
        try:
            curses.curs_set(1)  # Show cursor
        except curses.error:
            pass
        
        self.draw()
        
        while True:
            if not self.handle_input():
                break
            
            self.draw()
            
            # Small delay to reduce CPU usage
            time.sleep(0.01)


def main(stdscr, filename: Optional[str] = None):
    """Main entry point for curses application.
    
    Args:
        stdscr: Curses standard screen
        filename: Optional filename to load
    """
    editor = TextEditor(stdscr, filename)
    editor.run()


if __name__ == "__main__":
    import sys
    
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        curses.wrapper(main, filename)
    except KeyboardInterrupt:
        print("\nExited.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
