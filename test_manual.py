#!/usr/bin/env python3
"""
Manual test script to verify editor functionality.
This creates a mock test to verify key functionality works.
"""
import tempfile
import os
from text_autocomplete import TextEditor


class MockStdscr:
    """Mock curses screen for testing."""
    def __init__(self):
        self.nodelay_called = False
        self.keypad_called = False
        
    def nodelay(self, flag):
        self.nodelay_called = True
        
    def keypad(self, flag):
        self.keypad_called = True
        
    def getmaxyx(self):
        return (24, 80)  # Standard terminal size


# Mock curses module for testing
import curses
_original_init_pair = curses.init_pair

def mock_init_pair(*args, **kwargs):
    """Mock init_pair to avoid color errors."""
    try:
        return _original_init_pair(*args, **kwargs)
    except (ValueError, curses.error):
        pass  # Ignore color initialization errors in tests

curses.init_pair = mock_init_pair


def test_editor_initialization():
    """Test that editor can be initialized."""
    print("Testing editor initialization...")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content\nLine 2\nLine 3")
        temp_path = f.name
    
    try:
        mock_screen = MockStdscr()
        editor = TextEditor(mock_screen, temp_path)
        
        # Verify file was loaded
        assert len(editor.lines) == 3
        assert editor.lines[0] == "Test content"
        assert editor.lines[1] == "Line 2"
        assert editor.lines[2] == "Line 3"
        print("✓ Editor loads file correctly")
        
        # Test vim command execution
        result = editor.execute_vim_command("w")
        assert result == True  # Should continue running
        print("✓ Vim :w command works")
        
        # Test quit with modifications
        editor.modified = True
        result = editor.execute_vim_command("q")
        assert result == True  # Should warn and continue
        print("✓ Vim :q command warns on unsaved changes")
        
        # Test force quit
        result = editor.execute_vim_command("q!")
        assert result == False  # Should exit
        print("✓ Vim :q! command forces exit")
        
        # Test save function
        editor2 = TextEditor(mock_screen)
        editor2.lines = ["New content"]
        editor2.modified = True
        result = editor2.save_file()
        assert result == True
        assert editor2.filename == "untitled.txt"
        print("✓ Save function defaults to untitled.txt")
        
        # Clean up
        if os.path.exists("untitled.txt"):
            os.unlink("untitled.txt")
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    print("✓ All manual tests passed!\n")


if __name__ == "__main__":
    print("Running Manual Tests\n")
    print("=" * 50)
    
    try:
        test_editor_initialization()
        print("=" * 50)
        print("✓ Manual tests completed successfully!")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
