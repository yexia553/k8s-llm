# K8S-LLM

[中文](./README-zh.md)

A command-line tool that allows users to interact with Kubernetes using natural language, powered by Large Language Models.

## Features

- Natural language interface for Kubernetes commands
- Context-aware conversations
- Configurable LLM settings
- Command history and context management

## Installation

```bash
git clone git@github.com:yexia553/k8sllm.git
cd k8sllm
pip install -r requirements.txt && pip install . e
```

## Usage

```bash
# Ask a question
k8sllm -q "list all pods in the default namespace"

# Clear conversation context
k8sllm -c
```

You can also set `alias` to make usage easier.

```bash
alias qk8sllm='k8sllm -q'
alias ck8sllm='k8sllm -c'
```

After setting the above `alias`, you can directly use `qk8sllm` and `ck8sllm`.

```bash
# Ask a question
qk8sllm "List all pods in the default namespace"

# Clear conversation context
ck8sllm
```

## Configuration

Create a `.k8sllm/config.yaml` file in your home directory with the following structure:

```yaml
llm:
  base_url: "https://api.deepseek.com/v1" # Change this to your LLM service URL
  api_key: "your-api-key"
  model: "deepseek-chat" # Change this to your model name
```

Any large model API compatible with the OpenAI SDK can be used. Personally, I recommend DeepSeek as it offers good performance, is cost-effective, and has a simple configuration.

## Development

This project uses Python 3.8+ and requires the following main dependencies:

- click: For CLI interface
- pyyaml: For configuration management
- openai: For LLM integration

## License

MIT License
