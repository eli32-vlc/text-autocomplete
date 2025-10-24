"""
Configuration management module for text autocomplete.
"""
import json
import os
from typing import Dict, Any


class Config:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        "api_endpoint": "https://api.openai.com/v1",
        "api_key": "",
        "model": "gpt-4",
        "max_tokens": 30,
        "temperature": 0.7,
        "pause_delay_ms": 200
    }
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.
        
        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
            except (json.JSONDecodeError, IOError) as e:
                # Fall back to default config if error
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError:
            pass  # Ignore save errors
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value and save.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        self._save_config(self.config)
    
    @property
    def api_endpoint(self) -> str:
        """Get API endpoint."""
        return self.config.get("api_endpoint", "")
    
    @property
    def api_key(self) -> str:
        """Get API key."""
        return self.config.get("api_key", "")
    
    @property
    def model(self) -> str:
        """Get model name."""
        return self.config.get("model", "gpt-4")
    
    @property
    def max_tokens(self) -> int:
        """Get max tokens."""
        return self.config.get("max_tokens", 30)
    
    @property
    def temperature(self) -> float:
        """Get temperature."""
        return self.config.get("temperature", 0.7)
    
    @property
    def pause_delay_ms(self) -> int:
        """Get pause delay in milliseconds."""
        return self.config.get("pause_delay_ms", 200)
