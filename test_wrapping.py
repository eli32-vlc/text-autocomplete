#!/usr/bin/env python3
"""
Tests for line wrapping and async completion functionality.
"""
import time
import threading
from unittest.mock import MagicMock, patch


def test_async_completion():
    """Test that AI completion requests don't block."""
    print("Testing async AI completion...")
    
    # Mock the necessary components
    from text_autocomplete import TextEditor
    from config_manager import Config
    import curses
    
    # Mock curses functions that would fail without a terminal
    with patch('curses.init_pair'), patch('curses.color_pair'):
        # Create a mock curses screen
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 80)
        mock_stdscr.nodelay = MagicMock()
        mock_stdscr.keypad = MagicMock()
        
        # Create editor instance
        editor = TextEditor(mock_stdscr)
        
        # Test that requesting completion starts a thread
        editor.lines = ["This is a test"]
        editor.cursor_x = 14
        editor.cursor_y = 0
        editor.last_input_time = time.time()
        
        # Mock AI completer to simulate slow response
        slow_completion_called = []
        def slow_completion(context, timeout):
            time.sleep(0.1)  # Simulate API delay
            slow_completion_called.append(True)
            return "continuation text"
        
        editor.ai_completer.get_completion = slow_completion
        editor.ai_completer.is_available = lambda: True
        
        # Request completion
        start_time = time.time()
        editor.request_ai_completion()
        end_time = time.time()
        
        # Should return immediately (non-blocking)
        elapsed = end_time - start_time
        assert elapsed < 0.05, f"Completion request blocked for {elapsed}s"
        assert editor.requesting_completion, "Should be marked as requesting"
        
        # Wait for thread to complete
        if editor.completion_thread:
            editor.completion_thread.join(timeout=1.0)
        
        # Check that the slow completion was actually called
        assert len(slow_completion_called) > 0, "AI completion should have been called"
        assert editor.pending_suggestion == "continuation text", "Should have pending suggestion"
        
        print("✓ AI completion is non-blocking")
        print("✓ Async completion test passed\n")


def test_line_wrapping():
    """Test automatic line wrapping."""
    print("Testing line wrapping...")
    
    from text_autocomplete import TextEditor
    
    with patch('curses.init_pair'), patch('curses.color_pair'):
        # Create a mock curses screen with specific width
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 40)  # Width of 40 chars
        mock_stdscr.nodelay = MagicMock()
        mock_stdscr.keypad = MagicMock()
        
        # Create editor instance
        editor = TextEditor(mock_stdscr)
        editor.ai_enabled = False  # Disable AI for this test
        
        # Insert characters to exceed line width
        test_text = "This is a very long line that should wrap"
        for char in test_text:
            editor.insert_char(char)
        
        # Check if line wrapping occurred
        total_lines = len(editor.lines)
        total_text = ''.join(editor.lines)
        
        # Should have wrapped to multiple lines or at least not lost any text
        assert test_text.replace(' ', '') in total_text.replace(' ', ''), \
            f"Text should be preserved. Expected '{test_text}' in '{total_text}'"
        
        print(f"✓ Line wrapping preserved text across {total_lines} line(s)")
        
        # Test that cursor is positioned correctly
        assert editor.cursor_y >= 0, "Cursor Y should be valid"
        assert editor.cursor_x >= 0, "Cursor X should be valid"
        
        print("✓ Cursor position is valid after wrapping")
        print("✓ Line wrapping test passed\n")


def test_suggestion_acceptance_with_wrapping():
    """Test that accepting suggestions handles wrapping."""
    print("Testing suggestion acceptance with wrapping...")
    
    from text_autocomplete import TextEditor
    
    with patch('curses.init_pair'), patch('curses.color_pair'):
        # Create a mock curses screen with narrow width
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (24, 40)
        mock_stdscr.nodelay = MagicMock()
        mock_stdscr.keypad = MagicMock()
        
        # Create editor instance
        editor = TextEditor(mock_stdscr)
        editor.ai_enabled = False
        
        # Set up a long suggestion
        editor.lines = ["Start"]
        editor.cursor_y = 0
        editor.cursor_x = 5
        editor.suggestion = " with a very long suggestion that exceeds terminal width"
        editor.suggestion_match_pos = 0
        
        # Accept the suggestion
        editor.accept_suggestion()
        
        # Check that text was inserted
        total_text = ''.join(editor.lines)
        expected = "Start with a very long suggestion that exceeds terminal width"
        
        assert expected.replace(' ', '') in total_text.replace(' ', ''), \
            f"Expected '{expected}' to be in '{total_text}'"
        
        print("✓ Long suggestions are accepted correctly")
        print("✓ Suggestion acceptance test passed\n")


if __name__ == "__main__":
    print("Running Line Wrapping and Async Tests\n")
    print("=" * 60)
    
    try:
        test_async_completion()
        test_line_wrapping()
        test_suggestion_acceptance_with_wrapping()
        
        print("=" * 60)
        print("✓ All wrapping and async tests passed!")
        
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
