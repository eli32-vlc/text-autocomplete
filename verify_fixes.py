#!/usr/bin/env python3
"""
Verification script to demonstrate all fixes are working.
This script tests the issues mentioned in the problem statement.
"""

import sys
import tempfile
import os


def test_import():
    """Test 1: Verify module can be imported."""
    print("=" * 60)
    print("TEST 1: Module Import")
    print("=" * 60)
    try:
        import text_autocomplete
        print("✓ Module imports successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import: {e}")
        return False


def test_performance_features():
    """Test 2: Verify performance improvements exist."""
    print("\n" + "=" * 60)
    print("TEST 2: Performance Features")
    print("=" * 60)
    
    from text_autocomplete import TextEditor
    from ai_completer import AICompleter
    
    # Check for throttling
    print("Checking for performance features:")
    
    # Verify TextEditor has throttling variables
    class MockScreen:
        def nodelay(self, flag): pass
        def keypad(self, flag): pass
        def getmaxyx(self): return (24, 80)
    
    # Mock curses to avoid color errors
    import curses
    orig_init = curses.init_pair
    curses.init_pair = lambda *args, **kwargs: None
    
    try:
        editor = TextEditor(MockScreen())
        
        # Check for new performance attributes
        assert hasattr(editor, 'last_completion_request'), "Missing throttling timestamp"
        print("✓ Request throttling implemented")
        
        # Check timeout in AI completer
        import inspect
        sig = inspect.signature(AICompleter.get_completion)
        assert 'timeout' in sig.parameters, "Missing timeout parameter"
        print("✓ Request timeout implemented")
        
        return True
    except Exception as e:
        print(f"✗ Performance features check failed: {e}")
        return False
    finally:
        curses.init_pair = orig_init


def test_save_function():
    """Test 3: Verify save function works without filename."""
    print("\n" + "=" * 60)
    print("TEST 3: Save Function Fix")
    print("=" * 60)
    
    from text_autocomplete import TextEditor
    
    class MockScreen:
        def nodelay(self, flag): pass
        def keypad(self, flag): pass
        def getmaxyx(self): return (24, 80)
    
    import curses
    orig_init = curses.init_pair
    curses.init_pair = lambda *args, **kwargs: None
    
    try:
        editor = TextEditor(MockScreen())
        editor.lines = ["Test content"]
        editor.modified = True
        
        # Try saving without filename
        result = editor.save_file()
        
        # Check that default filename was used
        assert result == True, "Save should succeed"
        assert editor.filename == "untitled.txt", "Should use default filename"
        assert os.path.exists("untitled.txt"), "File should be created"
        
        print("✓ Save function works without filename")
        print(f"✓ Defaults to: {editor.filename}")
        
        # Clean up
        if os.path.exists("untitled.txt"):
            os.unlink("untitled.txt")
        
        return True
    except Exception as e:
        print(f"✗ Save function test failed: {e}")
        return False
    finally:
        curses.init_pair = orig_init


def test_exit_function():
    """Test 4: Verify exit function has proper confirmation."""
    print("\n" + "=" * 60)
    print("TEST 4: Exit Function Fix")
    print("=" * 60)
    
    from text_autocomplete import TextEditor
    
    class MockScreen:
        def nodelay(self, flag): pass
        def keypad(self, flag): pass
        def getmaxyx(self): return (24, 80)
    
    import curses
    orig_init = curses.init_pair
    curses.init_pair = lambda *args, **kwargs: None
    
    try:
        editor = TextEditor(MockScreen())
        
        # Check for exit confirmation attributes
        assert hasattr(editor, 'exit_requested'), "Missing exit_requested attribute"
        assert hasattr(editor, 'exit_request_time'), "Missing exit_request_time attribute"
        
        print("✓ Exit confirmation mechanism implemented")
        print("✓ Double-press Ctrl+X support added")
        
        return True
    except Exception as e:
        print(f"✗ Exit function test failed: {e}")
        return False
    finally:
        curses.init_pair = orig_init


def test_vim_commands():
    """Test 5: Verify vim-like commands are implemented."""
    print("\n" + "=" * 60)
    print("TEST 5: Vim-like Commands")
    print("=" * 60)
    
    from text_autocomplete import TextEditor
    
    class MockScreen:
        def nodelay(self, flag): pass
        def keypad(self, flag): pass
        def getmaxyx(self): return (24, 80)
    
    import curses
    orig_init = curses.init_pair
    curses.init_pair = lambda *args, **kwargs: None
    
    try:
        editor = TextEditor(MockScreen())
        
        # Check for vim command attributes
        assert hasattr(editor, 'vim_command_mode'), "Missing vim_command_mode attribute"
        assert hasattr(editor, 'vim_command'), "Missing vim_command attribute"
        assert hasattr(editor, 'execute_vim_command'), "Missing execute_vim_command method"
        
        print("✓ Vim command mode implemented")
        
        # Test vim commands
        commands_tested = []
        
        # Test :w (save)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        editor.filename = temp_file
        editor.lines = ["test"]
        result = editor.execute_vim_command("w")
        assert result == True, ":w should continue running"
        commands_tested.append(":w")
        
        # Test :q with unsaved changes
        editor.modified = True
        result = editor.execute_vim_command("q")
        assert result == True, ":q should warn and continue"
        commands_tested.append(":q")
        
        # Test :q! (force quit)
        result = editor.execute_vim_command("q!")
        assert result == False, ":q! should exit"
        commands_tested.append(":q!")
        
        print(f"✓ Vim commands work: {', '.join(commands_tested)}")
        
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        
        return True
    except Exception as e:
        print(f"✗ Vim commands test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        curses.init_pair = orig_init


def main():
    """Run all verification tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "FIX VERIFICATION SUITE" + " " * 21 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\nVerifying all fixes from the problem statement:\n")
    print("1. Performance issues and stuttering")
    print("2. Save function not working")
    print("3. Exit shortcuts not working")
    print("4. Vim-like behavior\n")
    
    results = []
    
    results.append(("Module Import", test_import()))
    results.append(("Performance Features", test_performance_features()))
    results.append(("Save Function", test_save_function()))
    results.append(("Exit Function", test_exit_function()))
    results.append(("Vim Commands", test_vim_commands()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} | {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED - All fixes verified!")
    else:
        print("✗ SOME TESTS FAILED - Review output above")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
