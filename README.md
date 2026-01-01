# Comet-Hive-Agent

**Deterministic Shortcut Engine for Browser Automation**

A mathematically rigorous implementation of the Axiom JSON Schema for browser automation shortcuts, featuring verified citation tracking and deterministic execution logging.

## Overview

Comet-Hive-Agent provides a foundational framework for creating, registering, and executing browser automation shortcuts with complete auditability. Built on Python's standard library, it requires no external dependencies while maintaining enterprise-grade reliability.

## Core Features

- **Deterministic Execution**: Every shortcut action produces reproducible results with cryptographic verification
- **Citation Tracking**: Immutable verified citations with SHA-256 content hashing
- **JSON Schema Export**: Full compatibility with Axiom JSON Schema standards
- **Audit Trail**: Complete execution logging for compliance and debugging
- **Zero Dependencies**: Uses only Python standard library (3.7+)

## Architecture

### ShortcutNode

Represents a deterministic automation action:
- `node_id`: Unique identifier
- `pattern`: URL or DOM pattern to match
- `action`: Automation action to execute
- `confidence`: Execution confidence (0.0-1.0)
- `verified_citations`: Immutable citation references
- `design_implications`: Metadata for system design

### CometEngine

Core orchestration engine:
- `register_shortcut()`: Register validated shortcuts
- `execute_shortcut()`: Execute with full logging
- `export_schema()`: Generate Axiom JSON schema
- `get_execution_log()`: Retrieve audit trail

### VerifiedCitation

Cryptographically verified content references:
- `source_id`: Unique source identifier
- `content_hash`: SHA-256 hash of cited content
- `timestamp`: ISO 8601 creation timestamp
- `verification_method`: Hash algorithm used

## Installation

```bash
git clone https://github.com/AXI0MH1VE/Comet-Hive-Agent.git
cd Comet-Hive-Agent
```

No additional dependencies required.

## Usage

### Basic Example

```python
from comet_engine import CometEngine, ShortcutNode, create_citation

# Initialize engine
engine = CometEngine()

# Create citation
citation = create_citation(
    source_id="github_docs",
    content="GitHub notification optimization pattern"
)

# Register shortcut
node = ShortcutNode(
    node_id="github_notif_opt",
    pattern="github.com/notifications",
    action="bulk_mark_done",
    confidence=0.95,
    verified_citations=[citation],
    design_implications={"efficiency": "high"}
)

engine.register_shortcut(node)

# Execute shortcut
result = engine.execute_shortcut(
    "github_notif_opt",
    {"user": "test_user", "timestamp": "2025-01-01"}
)

print(result)
```

### Export Schema

```python
schema = engine.export_schema()
print(json.dumps(schema, indent=2))
```

## Testing

Run comprehensive unit tests:

```bash
python -m unittest test_comet_engine.py
```

Test coverage includes:
- Citation creation and immutability
- Node validation and confidence bounds
- Shortcut registration and execution
- Execution log tracking
- Schema export integrity

## Design Principles

1. **Determinism**: Every execution produces identical results given identical inputs
2. **Immutability**: Citations and logs are cryptographically verified and immutable
3. **Auditability**: Complete execution trails for compliance and debugging
4. **Simplicity**: Zero external dependencies, pure Python implementation
5. **Extensibility**: Clean interfaces for integration with browser automation tools

## Axiom JSON Schema

Comet-Hive-Agent implements the Axiom JSON Schema specification for browser automation shortcuts. The schema ensures:

- Verified citations for all automation patterns
- Design implications metadata for system optimization
- Mathematical rigor in confidence scoring
- Complete auditability of all actions

## Project Structure

```
Comet-Hive-Agent/
├── comet_engine.py          # Core engine implementation
├── test_comet_engine.py     # Comprehensive unit tests
├── requirements.txt         # Dependencies (stdlib only)
└── README.md               # This file
```

## License

MIT License - See repository for details

## Contributing

Contributions welcome. Ensure:
- All tests pass
- Code maintains zero external dependencies
- Determinism is preserved
- Citations are cryptographically verified

## About

Developed as part of the Axiom Hive deterministic AI framework.

**Repository**: https://github.com/AXI0MH1VE/Comet-Hive-Agent
