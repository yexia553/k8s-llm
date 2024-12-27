"""
Configuration management for k8sllm.

This module handles loading and managing configuration settings from the
.k8sllm/config.yaml file, including LLM API keys and other settings.
"""

import os
import yaml
from pathlib import Path

class Config:
    """Configuration manager for k8sllm."""
    
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.k8sllm")
        self.config_file = os.path.join(self.config_dir, "config.yaml")
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_file):
            self._create_default_config()
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def _create_default_config(self):
        """Create default configuration file if it doesn't exist."""
        default_config = {
            'llm': {
                'base_url': 'https://api.deepseek.com/v1',
                'api_key': '',
                'model': 'deepseek-coder'
            }
        }

        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, 'w') as f:
            yaml.dump(default_config, f)

    def get_llm_config(self):
        """Get LLM-related configuration."""
        return self.config.get('llm', {})
