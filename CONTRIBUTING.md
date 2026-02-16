# Contributing to LLM-Driven Text Adventure RPG

Thank you for considering contributing to this project! We welcome contributions from everyone.

## 🎯 Ways to Contribute

### 1. Report Bugs
If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Ollama version)
- Game state (if applicable and non-sensitive)

### 2. Suggest Features
Have an idea for a new feature? Open an issue with:
- Clear description of the feature
- Use case/motivation
- Potential implementation approach (optional)

### 3. Submit Code
We accept pull requests! Please:
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Follow the coding standards below
- Write clear commit messages
- Test your changes
- Submit a pull request

## 📝 Coding Standards

### Python Style Guide
- Follow PEP 8 conventions
- Use type hints where applicable
- Write docstrings for all functions and classes (Google style)
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

### Example Function:
```python
def calculate_damage(attacker_strength: int, defender_defense: int) -> int:
    """
    Calculate damage dealt in combat.
    
    Args:
        attacker_strength (int): Strength stat of attacker
        defender_defense (int): Defense stat of defender
    
    Returns:
        int: Total damage dealt (minimum 1)
    """
    base_damage = max(1, attacker_strength - defender_defense)
    return base_damage
```

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests liberally

Example:
```
Add combat system with dice rolling

- Implement d20 combat mechanics
- Add critical hit detection
- Update game_engine.py with combat logic
- Add tests for damage calculation

Closes #42
```

## 🧪 Testing

Before submitting a PR:

1. **Manual Testing**: Play through your changes
   ```bash
   python main.py
   ```

2. **Code Style**: Check with pylint or flake8
   ```bash
   pylint main.py game_engine.py llm_parser.py
   ```

3. **Type Checking**: Run mypy (optional but recommended)
   ```bash
   mypy main.py game_engine.py llm_parser.py
   ```

## 🗂️ Project Structure Guidelines

### File Organization
```
llm_rpg/
├── main.py              # Keep UI/display logic here
├── game_engine.py       # State management only
├── llm_parser.py        # LLM communication only
├── game_data/           # JSON data files
└── tests/               # Test files (if adding)
```

### Adding New Features

**For new game mechanics:**
1. Add logic to `game_engine.py`
2. Update JSON schema in `llm_parser.py` prompt
3. Update display logic in `main.py`
4. Update `initial_state.json` if needed

**For new locations/NPCs:**
1. Edit `game_data/initial_state.json`
2. Follow existing JSON structure
3. Ensure all required fields are present

## 🚀 Pull Request Process

1. Update README.md if you're adding user-facing features
2. Update this CONTRIBUTING.md if you're changing dev workflow
3. Ensure your code passes all checks
4. Request review from maintainers
5. Address review feedback
6. Maintainer will merge when approved

## 🎨 Design Principles

When contributing, keep these principles in mind:

1. **Simplicity**: Keep the codebase simple and readable
2. **Modularity**: Separate concerns (UI, logic, AI)
3. **Extensibility**: Make it easy to add new features
4. **Robustness**: Handle errors gracefully
5. **User Experience**: Prioritize clear, helpful feedback

## 📚 Learning Resources

New to contributing to open source? Check out:
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Contributions](https://github.com/firstcontributions/first-contributions)
- [PEP 8 Style Guide](https://pep8.org/)

## 🤝 Code of Conduct

Be respectful and constructive in all interactions. We're all here to learn and build something cool together.

## ❓ Questions?

Don't hesitate to ask! Open an issue with the "question" label or reach out to maintainers.

---

**Thank you for contributing to LLM-Driven Text Adventure RPG!** 🗡️✨
