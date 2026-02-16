# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## 🏃 Express Setup

### Step 1: Prerequisites
```bash
# Check Python version (need 3.9+)
python --version

# Install Ollama from https://ollama.ai/
# Then pull the model:
ollama pull qwen2.5:14b
```

### Step 2: Install
```bash
# Clone and navigate
git clone <your-repo-url>
cd llm_rpg

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Setup
```bash
python setup_check.py
```

Should show all ✅ checks passed!

### Step 4: Play!
```bash
python main.py
```

## 🎮 First Actions to Try

Once the game starts, try these commands:

```
> look around
> take the rusty dagger
> examine the old map
> go north
> talk to the mysterious traveler
```

## 💡 Tips

- **Be natural**: Type commands like you're talking to a friend
- **Combine actions**: "Pick up the dagger and head north" works!
- **Save automatically**: Game saves after each turn
- **Type 'help'**: For in-game assistance
- **Type 'quit'**: To save and exit

## 🔧 Common Issues

### "Ollama not found"
Install Ollama from https://ollama.ai/

### "Model not found"
Run: `ollama pull qwen2.5:14b`

### "Game runs slow"
Qwen2.5-14B needs good hardware. Consider:
- Using `qwen2.5:7b` instead (edit `llm_parser.py` line 17)
- Ensuring 16GB+ RAM
- Closing other applications

## 📖 Full Documentation

For detailed info, see [README.md](README.md)

---

**Ready? Let's adventure!** 🗡️✨
