"""
AI completion module for text autocomplete.
"""
import json
import time
from typing import Optional
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class AICompleter:
    """Handles AI-powered text completion."""
    
    def __init__(self, config):
        """Initialize AI completer.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.client = None
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Minimum seconds between requests
        
        if OpenAI is not None and config.api_key:
            try:
                self.client = OpenAI(
                    api_key=config.api_key,
                    base_url=config.api_endpoint
                )
            except Exception:
                self.client = None
    
    def get_completion(self, text: str) -> Optional[str]:
        """Get AI completion for given text.
        
        Args:
            text: Text to complete
            
        Returns:
            Completion string or None if unavailable
        """
        if not self.client or not text.strip():
            return None
        
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_request_time < self.min_request_interval:
            return None
        
        self.last_request_time = current_time
        
        try:
            # Create a prompt that asks for natural continuation
            prompt = f"{text}"
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful writing assistant. Continue the given text naturally. Only provide the continuation, not the original text. Keep it concise and relevant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stream=False
            )
            
            if response.choices and len(response.choices) > 0:
                completion = response.choices[0].message.content
                if completion:
                    # Clean up the completion
                    completion = completion.strip()
                    # Remove any markdown or formatting
                    if completion.startswith('"') and completion.endswith('"'):
                        completion = completion[1:-1]
                    return completion
            
            return None
            
        except Exception as e:
            # Silently fail on API errors
            return None
    
    def is_available(self) -> bool:
        """Check if AI completion is available.
        
        Returns:
            True if client is configured, False otherwise
        """
        return self.client is not None
