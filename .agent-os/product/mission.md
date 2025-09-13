# Product Mission

## Pitch

Penpal is an AI agent management application that helps developers and tinkerers create and interact with multiple AI agents by providing agent-centric design with unprecedented model support and hackability.

## Users

### Primary Customers

- **Developers and Tinkerers**: Technical users who want to experiment with different AI models and agent configurations
- **AI Enthusiasts**: Users who want to create specialized AI agents for different purposes with full control over their setup

### User Personas

**Jeffery** (30-50 years old)
- **Role:** Developer/Dilettante/Tinkerer
- **Context:** Personal projects and experimentation with AI technologies
- **Pain Points:** Existing AI applications are chat-oriented rather than agent-focused, limited model support, difficult to customize and extend
- **Goals:** Create multiple specialized AI agents, experiment with different models and configurations, maintain full control and portability of agent data

## The Problem

### Limited Agent Management

Most AI applications focus on chat interfaces rather than agent creation and management. Users can't easily create, configure, and maintain multiple specialized AI agents with different personalities, tools, and purposes.

**Our Solution:** Penpal provides an agent-centric design where users create agents first with full customization options.

### Restricted Model Access

Current AI applications typically support only one or two model providers, limiting user choice and experimentation opportunities.

**Our Solution:** Penpal offers ridiculous model support with BYOK connectivity to major providers plus local inference options, providing access to approximately 400 different models.

### Poor Hackability

Many AI applications use proprietary technologies or complex architectures that make customization and extension difficult for developers.

**Our Solution:** Penpal uses common, widely-known technologies (TypeScript, Python, Electron) making it trivial to tinker with and extend.

## Differentiators

### Agent-First Architecture

Unlike chat-oriented AI applications, Penpal puts agent creation and management at the center of the user experience. Each agent is a complete entity with its own configuration, conversation history, and portable SQLite database.

### Unprecedented Model Support

Unlike applications limited to one or two providers, Penpal supports BYOK connections to Anthropic, OpenAI, Google, Groq, OpenRouter, plus local inference through Ollama and LM Studio, offering access to hundreds of models.

### Maximum Hackability

Unlike applications built with proprietary or complex technologies, Penpal uses the most common web technologies (TypeScript frontend, Python backend, Electron shell) making it extremely easy to modify and extend.

## Key Features

### Core Features

- **Agent Creation & Management:** Create unlimited AI agents with custom names, models, system prompts, and tool configurations
- **Portable Agent Storage:** Each agent stored in its own SQLite .db file for maximum portability and data ownership
- **Multi-Provider Model Support:** BYOK connectivity to Anthropic, OpenAI, Google, Groq, and OpenRouter
- **Local Model Integration:** Support for local LLM inference through Ollama and LM Studio
- **Agent-Centric Interface:** Navigate and interact with agents as primary entities rather than conversations

### Advanced Features

- **Custom Tool Integration:** Assign specific tools and capabilities to individual agents
- **Conversation History Management:** Complete conversation history preserved per agent with full search capabilities
- **Model Switching:** Change models for existing agents without losing conversation context
- **Configuration Export/Import:** Share agent configurations and clone successful setups
- **Developer-Friendly Architecture:** Built with TypeScript, Python, and Electron for easy customization