#!/usr/bin/env python3
"""
Demo script to show the text autocomplete application structure.
Since curses requires an interactive terminal, this script demonstrates
the key features without running the full TUI.
"""
import os
import json
from config_manager import Config
from ai_completer import AICompleter


def demo_config():
    """Demonstrate configuration management."""
    print("=" * 60)
    print("1. CONFIGURATION MANAGEMENT")
    print("=" * 60)
    
    # Create example config if it doesn't exist
    if not os.path.exists('config.json'):
        print("\n📝 Creating config.json from example...")
        with open('config.example.json', 'r') as src:
            with open('config.json', 'w') as dst:
                dst.write(src.read())
        print("✓ Config file created")
    
    # Load config
    config = Config()
    print(f"\n📋 Current Configuration:")
    print(f"  • API Endpoint: {config.api_endpoint}")
    print(f"  • Model: {config.model}")
    print(f"  • Max Tokens: {config.max_tokens}")
    print(f"  • Temperature: {config.temperature}")
    print(f"  • Pause Delay: {config.pause_delay_ms}ms")
    
    if not config.api_key or config.api_key == "your-api-key-here":
        print(f"  • API Key: ⚠️  NOT CONFIGURED")
        print("\n💡 To enable AI features, edit config.json and add your API key")
    else:
        print(f"  • API Key: ✓ Configured")


def demo_ai_completer():
    """Demonstrate AI completer initialization."""
    print("\n" + "=" * 60)
    print("2. AI COMPLETER")
    print("=" * 60)
    
    config = Config()
    completer = AICompleter(config)
    
    if completer.is_available():
        print("\n✓ AI Completer is ready")
        print("  The application will provide real-time suggestions as you type")
    else:
        print("\n⚠️  AI Completer is not available")
        print("  Reason: API key not configured or OpenAI library not available")
        print("\n  To enable AI features:")
        print("  1. Edit config.json")
        print("  2. Set your OpenAI API key")
        print("  3. Optionally configure custom endpoint and model")


def demo_features():
    """Demonstrate key features."""
    print("\n" + "=" * 60)
    print("3. KEY FEATURES")
    print("=" * 60)
    
    features = [
        ("📝 Nano-like Interface", "Familiar text editor with status bar and help text"),
        ("🤖 AI Autocomplete", "Real-time word/phrase predictions as you type"),
        ("👻 Ghost Text", "Suggestions appear in faint cyan color"),
        ("⌨️  Easy Acceptance", "Press Tab or Right Arrow to accept suggestions"),
        ("🎯 Smart Matching", "Continue typing - suggestions update intelligently"),
        ("💾 File Operations", "Save and load text files with Ctrl+S and Ctrl+O"),
        ("🔄 Toggle AI", "Press Ctrl+G to enable/disable AI suggestions"),
        ("⚡ Pause Detection", "Suggestions trigger after brief pause (200ms default)"),
    ]
    
    print("\n")
    for icon_title, description in features:
        print(f"  {icon_title}")
        print(f"    → {description}")
        print()


def demo_usage():
    """Show usage examples."""
    print("=" * 60)
    print("4. USAGE")
    print("=" * 60)
    
    print("\n📚 Starting the editor:")
    print("  $ python3 text_autocomplete.py")
    print("  $ python3 text_autocomplete.py myfile.txt")
    
    print("\n⌨️  Keyboard Controls:")
    controls = [
        ("Ctrl+S", "Save current file"),
        ("Ctrl+O", "Open a file"),
        ("Ctrl+X", "Exit editor"),
        ("Ctrl+G", "Toggle AI autocomplete on/off"),
        ("Tab", "Accept AI suggestion"),
        ("Right Arrow", "Accept AI suggestion (or move cursor if no suggestion)"),
        ("Arrow Keys", "Navigate text"),
        ("Backspace", "Delete character"),
    ]
    
    for key, action in controls:
        print(f"  {key:15} → {action}")
    
    print("\n📖 Example Workflow:")
    workflow = [
        "1. Start typing: 'The quick brown'",
        "2. Pause briefly (200ms)",
        "3. AI suggests: 'fox jumps over the lazy dog' (shown in ghost text)",
        "4. Press Tab to accept, or keep typing to refine",
        "5. If you type 'f' and it matches suggestion, it stays",
        "6. If you type 'c' (doesn't match), suggestion refreshes",
    ]
    
    for step in workflow:
        print(f"  {step}")


def demo_architecture():
    """Show architecture overview."""
    print("\n" + "=" * 60)
    print("5. ARCHITECTURE")
    print("=" * 60)
    
    print("\n📦 Project Structure:")
    files = [
        ("text_autocomplete.py", "Main TUI editor with curses"),
        ("config_manager.py", "Configuration loader and manager"),
        ("ai_completer.py", "AI completion via OpenAI API"),
        ("config.json", "User configuration file"),
        ("requirements.txt", "Python dependencies"),
    ]
    
    for filename, description in files:
        print(f"  {filename:25} - {description}")
    
    print("\n🔄 How It Works:")
    print("""
  1. User types text in the editor
  2. Each keystroke updates the text buffer
  3. After pause (200ms), editor captures context before cursor
  4. Context sent to AI model (via OpenAI API)
  5. AI returns completion prediction
  6. Prediction displayed as ghost text at cursor position
  7. User accepts (Tab) or continues typing
  8. If typing matches suggestion → keeps suggestion
  9. If typing diverges → requests new suggestion
    """)


def main():
    """Main demo function."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  TEXT AUTOCOMPLETE - AI-Powered Text Editor".center(58) + "║")
    print("║" + "  Like GitHub Copilot, but for words!".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    demo_config()
    demo_ai_completer()
    demo_features()
    demo_usage()
    demo_architecture()
    
    print("\n" + "=" * 60)
    print("🚀 READY TO USE")
    print("=" * 60)
    print("\nTo start the application, run:")
    print("  $ python3 text_autocomplete.py")
    print("\nTo open a file directly:")
    print("  $ python3 text_autocomplete.py myfile.txt")
    print("\n⚠️  Note: Requires a terminal with curses support")
    print("   (works on Linux/macOS, Windows needs windows-curses)")
    print("\n💡 Configure your API key in config.json to enable AI features")
    print("\n")


if __name__ == "__main__":
    main()
