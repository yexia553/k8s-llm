"""
Kubernetes Executor module for k8sllm.

This module is responsible for executing Kubernetes commands
and handling their results. It provides a safe interface for
running kubectl commands generated from natural language queries.
"""

import subprocess
import shlex

class K8sExecutor:
    """Executes Kubernetes commands and handles their output."""

    def execute(self, command, is_dangerous=False):
        """
        Execute a Kubernetes command and return its output.
        
        Args:
            command (str): The kubectl command to execute
            is_dangerous (bool): Whether the command is potentially dangerous
            
        Returns:
            tuple: (output, requires_confirmation)
                - output (str): Command output or message
                - requires_confirmation (bool): Whether user confirmation is needed
        """
        try:
            # Add kubectl if not present
            if not command.startswith('kubectl'):
                command = f'kubectl {command}'
            
            # For dangerous commands, return early with confirmation request
            if is_dangerous:
                return (
                    f"⚠️  This is a potentially dangerous operation!\n"
                    f"Command to be executed: {command}\n"
                    f"Please confirm you want to proceed (y/n): ",
                    True
                )
                
            # Execute the command and capture output
            args = shlex.split(command)
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero exit
            )
            
            # Combine stdout and stderr, with stdout first
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                if output:
                    output += "\n"
                output += result.stderr
                
            return output, False
            
        except Exception as e:
            return f"Error: {str(e)}", False

    def execute_confirmed(self, command):
        """
        Execute a confirmed dangerous command.
        
        Args:
            command (str): The kubectl command to execute
            
        Returns:
            str: The command output or error message
        """
        try:
            args = shlex.split(command)
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero exit
            )
            
            # Combine stdout and stderr, with stdout first
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                if output:
                    output += "\n"
                output += result.stderr
                
            return output
            
        except Exception as e:
            return f"Error: {str(e)}"
