"""
Cliente de API para Groq con el modelo llama-3.1-8b.
"""

import os
from typing import Optional, List, Dict
from groq import Groq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class GroqClient:
    """Cliente para interactuar con el modelo llama-3.1-8b de Groq."""
    
    DEFAULT_MODEL = "llama-3.1-8b-instant"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de Groq.
        
        Args:
            api_key: API key de Groq. Si no se provee, busca GROQ_API_KEY en el entorno.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Se debe proveer una API key o configurar GROQ_API_KEY como variable de entorno")
        
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
        Envía una solicitud de chat al modelo.
        
        Args:
            messages: Lista de mensajes con claves 'role' y 'content'
            temperature: Parámetro de temperatura para el muestreo (0-2)
            max_tokens: Cantidad máxima de tokens a generar
            top_p: Parámetro top-p para el muestreo
            
        Returns:
            Contenido de la respuesta del modelo como string
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        
        if not completion.choices:
            raise ValueError("No se recibió respuesta de la API")
        
        content = completion.choices[0].message.content
        return content if content is not None else ""
    
    def simple_prompt(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Envía un prompt simple al modelo.
        
        Args:
            prompt: Mensaje del usuario
            system_message: Mensaje de sistema opcional para contexto
            
        Returns:
            Contenido de la respuesta del modelo como string
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages)
