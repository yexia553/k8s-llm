"""
Command Line Interface for k8sllm.

This module provides the main entry point for the k8sllm command-line tool.
It handles command-line arguments, configuration management, and orchestrates
the interaction between different components of the system.
"""

import click
from .config import Config
from .llm_processor import LLMProcessor
from .k8s_executor import K8sExecutor
from .context_manager import ContextManager

@click.command()
@click.argument('query', required=False)
@click.option('-q', '--query', 'option_query', help='Natural language query for Kubernetes operations')
@click.option('-c', '--clear-context', is_flag=True, help='Clear the conversation context')
def cli(query, option_query, clear_context):
    """K8sLLM - Natural language interface for Kubernetes."""
    if clear_context:
        config = Config()
        context_manager = ContextManager(config)
        context_manager.clear()
        click.echo("Context cleared successfully.")
        return

    # Use query from argument if provided, otherwise use from option
    final_query = query or option_query
    
    if not final_query:
        final_query = click.prompt('Enter your Kubernetes query')

    config = Config()
    context_manager = ContextManager(config)
    llm_processor = LLMProcessor(config)
    k8s_executor = K8sExecutor()

    # Process the query
    response_type, response = llm_processor.process_query(final_query, context_manager.get_context())
    
    if response_type == 'command':
        k8s_command, is_dangerous = response
        # Display the command with visual effects
        click.echo("Command to execute:")
        if is_dangerous:
            click.echo(click.style(f" {k8s_command}", fg='red', bold=True, bg='black'))
        else:
            click.echo(click.style(f" {k8s_command}", fg='green', bold=True))
        click.echo()  # Add a blank line for better readability
        
        # Execute the command
        result, requires_confirmation = k8s_executor.execute(k8s_command, is_dangerous)
        
        if requires_confirmation:
            click.echo(result)  # Print the confirmation message
            if click.confirm("Do you want to proceed?"):
                result = k8s_executor.execute_confirmed(k8s_command)
            else:
                result = "Operation cancelled by user."
    else:  # response_type == 'answer'
        result = response
        click.echo(click.style("\nAnswer:", bold=True))
        # click.echo(response)
        click.echo()
    
    # Update context with the result
    context_manager.update_context(final_query, result, result)
    
    # Display the result
    click.echo(result + "\n-------------------\n")

if __name__ == '__main__':
    cli()
