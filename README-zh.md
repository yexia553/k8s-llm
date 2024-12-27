# K8S-LLM

一个命令行工具，允许用户使用自然语言与 Kubernetes 进行交互，基于大型语言模型提供支持。

## 功能特点

- Kubernetes 命令的自然语言界面
- 上下文感知对话
- 可配置的 LLM 设置
- 命令历史和上下文管理

## 安装

```bash
git clone git@github.com:yexia553/k8sllm.git
cd k8sllm
pip install -r requirements.txt && pip install . e
```

## 使用方法

```bash
# 提问
k8sllm -q "列出默认命名空间中的所有 pod"

# 清除对话上下文
k8sllm -c
```

也可以设置`alias`,使用的时候更方便

```bash
alias qk8sllm='k8sllm -q'
alias ck8sllm='k8sllm -c'
```

设置了以上`alias`之后,可以直接使用`qk8sllm`和`ck8sllm`。

```bash
# 提问
qk8sllm "列出默认命名空间中的所有 pod"

# 清除对话上下文
ck8sllm
```

## 配置

在 用户的的根目录中创建一个 `.k8sllm/config.yaml` 文件，文件结构如下：

```yaml
llm:
  base_url: "https://api.deepseek.com/v1" # 更改为您的 LLM 服务 URL
  api_key: "your-api-key"
  model: "deepseek-chat" # 更改为您的模型名称
```

任何兼容 OpenAI SDK 的大模型 API 都可以使用。我个人推荐 DeepSeek，它提供良好的性能、价格便宜，并且配置简单。

## 开发

该项目使用 Python 3.8+，并需要以下主要依赖项：

- click：用于 CLI 接口
- pyyaml：用于配置管理
- openai：用于 LLM 集成

## License

MIT License
