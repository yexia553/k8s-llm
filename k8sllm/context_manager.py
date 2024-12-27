"""
Context Manager module for k8sllm.

This module manages the conversation context between the user and the LLM,
storing and retrieving previous interactions to maintain context awareness
during the conversation.
"""

import os
import json
from pathlib import Path

class ContextManager:
    """Manages conversation context for k8sllm."""

    def __init__(self, config):
        """Initialize context manager with configuration."""
        self.config = config
        self.context_file = os.path.expanduser("~/.k8sllm/context.json")
        self._ensure_context_file()

    def _ensure_context_file(self):
        """Ensure context file exists."""
        os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
        if not os.path.exists(self.context_file):
            self._save_context([])

    def _load_context(self):
        """Load context from file."""
        try:
            with open(self.context_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def _save_context(self, context):
        """Save context to file."""
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(context, f)

    def get_context(self):
        """
        Get the current conversation context.
        
        Returns:
            str: Formatted context string
        """
        context = self._load_context()
        if not context:
            return None
            
        # Format context for LLM consumption
        formatted_context = []
        for item in context[-5:]:  # Only use last 5 interactions
            formatted_context.extend([
                f"User: {item['query']}",
                f"Command: {item['command']}",
                f"Result: {item['result']}"
            ])
        return "\n".join(formatted_context)

    def update_context(self, query, command, result):
        """
        Update context with new interaction.
        
        Args:
            query (str): User's natural language query
            command (str): Executed kubectl command
            result (str): Command execution result
        """
        context = self._load_context()
        context.append({
            'query': query,
            'command': command,
            'result': result
        })
        # Keep only last 10 interactions
        context = context[-10:]
        self._save_context(context)

    def clear(self):
        """Clear all context."""
        self._save_context([])
