"""
Basic tests for text autocomplete modules.
"""
import os
import json
import tempfile
from config_manager import Config
from ai_completer import AICompleter


def test_config_manager():
    """Test configuration manager."""
    print("Testing Config Manager...")
    
    # Test with temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_config = {
            "api_endpoint": "https://test.example.com",
            "api_key": "test-key",
            "model": "test-model"
        }
        json.dump(test_config, f)
        temp_path = f.name
    
    try:
        config = Config(temp_path)
        
        assert config.api_endpoint == "https://test.example.com"
        assert config.api_key == "test-key"
        assert config.model == "test-model"
        assert config.max_tokens == 30  # Default value
        
        print("✓ Config loading works")
        
        # Test setting values
        config.set("max_tokens", 50)
        assert config.get("max_tokens") == 50
        
        print("✓ Config setting works")
        
    finally:
        os.unlink(temp_path)
    
    print("✓ Config Manager tests passed\n")


def test_ai_completer_init():
    """Test AI completer initialization."""
    print("Testing AI Completer...")
    
    # Test with no API key
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_config = {
            "api_endpoint": "https://api.openai.com/v1",
            "api_key": "",
            "model": "gpt-4"
        }
        json.dump(test_config, f)
        temp_path = f.name
    
    try:
        config = Config(temp_path)
        completer = AICompleter(config)
        
        # Should not be available without API key
        assert not completer.is_available()
        print("✓ AI Completer handles missing API key")
        
    finally:
        os.unlink(temp_path)
    
    print("✓ AI Completer tests passed\n")


def test_file_operations():
    """Test file save/load operations."""
    print("Testing File Operations...")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Line 1\nLine 2\nLine 3")
        temp_path = f.name
    
    try:
        # Test that file exists and can be read
        with open(temp_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            assert len(lines) == 3
            assert lines[0] == "Line 1"
        
        print("✓ File operations work")
        
    finally:
        os.unlink(temp_path)
    
    print("✓ File operation tests passed\n")


def test_vim_commands():
    """Test vim command parsing."""
    print("Testing Vim Command Support...")
    
    # We can't fully test the editor without a curses screen,
    # but we can verify the module loads without errors
    try:
        import text_autocomplete
        print("✓ Text autocomplete module loads successfully")
    except ImportError as e:
        print(f"✗ Failed to import module: {e}")
        raise
    
    print("✓ Vim command support tests passed\n")


if __name__ == "__main__":
    print("Running Text Autocomplete Tests\n")
    print("=" * 50)
    
    try:
        test_config_manager()
        test_ai_completer_init()
        test_file_operations()
        test_vim_commands()
        
        print("=" * 50)
        print("✓ All tests passed!")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
