# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-16

### 🎉 Initial Release

#### Added
- **Core Game Engine**
  - JSON-based state management system
  - Auto-save functionality after each turn
  - Support for player stats (health, gold, XP)
  - Inventory management with add/remove operations
  - Location system with dynamic room states

- **LLM Integration**
  - Ollama API integration with Qwen2.5-14B
  - Natural language command parsing
  - Structured JSON output validation
  - Error handling and retry logic
  - Schema-strict update system

- **Game World**
  - 5 unique locations (Rusty Cave, Forest Path, Village Square, Blacksmith Forge, Village Inn)
  - 6 NPCs with dialogue systems
  - Quest tracking framework
  - Item system with multiple collectibles
  - Dynamic entity interactions

- **User Interface**
  - Colorful emoji-enhanced CLI display
  - Location descriptions with atmospheric details
  - Real-time stat display
  - Action feedback system
  - Help command and stats viewing

- **Documentation**
  - Comprehensive README.md with architecture diagrams
  - Quick Start guide for fast setup
  - Contributing guidelines
  - MIT License
  - Environment verification script

- **Developer Tools**
  - PEP 8 compliant code with type hints
  - Comprehensive docstrings
  - Modular architecture (main, engine, parser)
  - .gitignore for clean repository

#### Technical Details
- Python 3.9+ support
- Ollama client library integration
- JSON-based persistence
- Graceful error handling
- Extensible update system

---

## [Unreleased]

### 🔮 Planned Features
- [ ] Combat system with dice rolling
- [ ] Character creation and customization
- [ ] Procedural location generation
- [ ] Multi-language support
- [ ] Voice input integration
- [ ] Save slot management
- [ ] Achievement system
- [ ] More quests and storylines

---

## Version History

### Version Numbering
- **Major (X.0.0)**: Breaking changes, major features
- **Minor (1.X.0)**: New features, backward compatible
- **Patch (1.0.X)**: Bug fixes, minor improvements

---

**Note**: This changelog is maintained by hand. For detailed commit history, see `git log`.
