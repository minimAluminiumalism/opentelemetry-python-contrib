# Langchain Instrumentation Migration Guide

## Overview

This document explains how to migrate Langchain instrumentation from the openllmetry project to the opentelemetry-python-contrib project.

## Migration Strategy

### 1. Keep Code Changes Minimal

To facilitate future migration of all code, we adopted the following strategy:

- **Maintain original callback mechanism**: Continue using LangChain's BaseCallbackHandler mechanism
- **Maintain original span creation logic**: Keep the core logic of TraceloopCallbackHandler
- **Maintain original semantic conventions**: Use the same span attributes and metrics

### 2. Adapt to opentelemetry-python-contrib Structure

#### Project Structure Adaptation
```
opentelemetry-instrumentation-langchain/
├── src/opentelemetry/instrumentation/langchain/
│   ├── __init__.py              # Main instrumentor class
│   ├── callback_handler.py     # Core callback handling logic
│   ├── config.py               # Configuration class
│   ├── utils.py                # Utility functions
│   └── version.py              # Version information
├── tests/                      # Test files
├── examples/                   # Example code
├── pyproject.toml             # Project configuration
└── README.rst                 # Documentation
```

#### Dependency Adaptation
- Use `opentelemetry.semconv_ai` instead of custom semantic conventions package
- Adapt to opentelemetry-python-contrib build system (hatchling)
- Use official OpenTelemetry package versions

### 3. Key Changes

#### Semantic Conventions
- Migrate from `opentelemetry-semantic-conventions-ai` to `opentelemetry.semconv_ai`
- Keep the same attribute names and enum values

#### Build System
- Migrate from Poetry to Hatchling
- Adapt to opentelemetry-python-contrib version management

#### Import Strategy
- Use delayed imports to avoid importing langchain dependencies at module level
- Ensure instrumentation can be imported in environments without langchain

## Core Migrated Files

### 1. callback_handler.py
This is the most core file, containing all span creation and management logic:
- `TraceloopCallbackHandler` class
- Span attribute setting functions
- Error handling logic

### 2. __init__.py
Main instrumentor class:
- `LangchainInstrumentor` class
- Function wrapping logic
- OpenAI tracing wrapper

### 3. utils.py
Utility functions:
- JSON encoder
- Configuration functions
- Error handling decorators

## Usage

```python
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

# Enable instrumentation
LangchainInstrumentor().instrument()

# Now your Langchain applications will automatically generate traces
```

## Compatibility

- **Backward compatible**: Maintains the same API as original openllmetry instrumentation
- **Semantic compatible**: Generates the same span attributes and metrics
- **Feature compatible**: Supports the same Langchain components and operations

## Future Migration

This migration provides a template for future migration of other LLM instrumentations:

1. **Keep core logic unchanged**
2. **Adapt project structure**
3. **Update dependencies and build system**
4. **Use delayed import strategy**

Through this approach, all instrumentations in openllmetry can be quickly migrated to opentelemetry-python-contrib. 