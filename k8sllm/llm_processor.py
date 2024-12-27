"""
LLM Processing module for k8sllm.

This module handles the interaction with the Language Model API,
processing natural language queries and generating appropriate
Kubernetes commands based on the user's input.
"""

from openai import OpenAI

class LLMProcessor:
    """Processes natural language queries using LLM."""

    def __init__(self, config):
        """Initialize LLM processor with configuration."""
        self.config = config.get_llm_config()
        self.client = OpenAI(api_key=self.config['api_key'], base_url=self.config['base_url'])
        self.model = self.config['model']

    def process_query(self, query, context=None):
        """
        Process a natural language query and return the corresponding K8s command or answer.
        
        Args:
            query (str): The natural language query
            context (str, optional): Previous conversation context
            
        Returns:
            tuple: (response_type, response)
                - response_type (str): Either 'command' or 'answer'
                - response (str or tuple): The generated Kubernetes command or answer
        """
        # Construct the prompt
        system_prompt = """You are a Kubernetes expert. Analyze the user's query and respond appropriately:

            1. If the user is asking for a kubectl command or operation:
            - Convert the query into the appropriate kubectl command
            - Format your response exactly as:
            COMMAND: <the kubectl command>
            DANGEROUS: <true/false>

            2. If the user is asking a general question about Kubernetes:
            - Provide a clear and concise answer
            - Format your response exactly as:
            ANSWER: <your detailed explanation>
            
            IMPORTANT: always respond in Chinese
            """
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]

        if context:
            messages.append({"role": "user", "content": f"Previous context: {context}"})

        messages.append({"role": "user", "content": query})

        # Get response from LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,  # Low temperature for more deterministic outputs
        )

        # Parse the response
        response_text = response.choices[0].message.content.strip()
        command_line = next((line for line in response_text.split('\n') if line.startswith('COMMAND:')), '')
        answer_line = next((line for line in response_text.split('\n') if line.startswith('ANSWER:')), '')
        dangerous_line = next((line for line in response_text.split('\n') if line.startswith('DANGEROUS:')), '')
        
        if command_line:
            command = command_line.replace('COMMAND:', '').strip()
            is_dangerous = dangerous_line.replace('DANGEROUS:', '').strip().lower() == 'true'
            return 'command', (command, is_dangerous)
        elif answer_line:
            answer = answer_line.replace('ANSWER:', '').strip()
            return 'answer', answer
