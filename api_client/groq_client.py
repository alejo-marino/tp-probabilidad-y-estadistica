"""
Groq API Client for llama-3.1-8b model.
"""

import os
from typing import Optional, List, Dict
from groq import Groq


class GroqClient:
    """Client for interacting with Groq's llama-3.1-8b model."""
    
    DEFAULT_MODEL = "llama-3.1-8b-instant"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key. If not provided, will look for GROQ_API_KEY in environment.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in GROQ_API_KEY environment variable")
        
        self.client = Groq(api_key=self.api_key)
        self.model = self.DEFAULT_MODEL
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
    ) -> str:
        """
        Send a chat request to the model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum number of tokens to generate
            top_p: Top-p sampling parameter
            
        Returns:
            Model's response content as string
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        
        return completion.choices[0].message.content
    
    def simple_prompt(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Send a simple prompt to the model.
        
        Args:
            prompt: User prompt
            system_message: Optional system message to set context
            
        Returns:
            Model's response content as string
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages)
