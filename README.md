# 🗡️ LLM-Driven Text Adventure RPG

> **A next-generation text adventure game powered by Qwen2.5-14B as a Semantic World Engine**

Transform natural language commands into dynamic game state changes using advanced AI. This project demonstrates how Large Language Models can serve as intelligent game masters, interpreting player intent and managing complex world states in real-time.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-Qwen2.5--14B-green.svg)](https://ollama.ai/)

---

## 🎮 What Makes This Special?

Unlike traditional text adventures with rigid command parsers, this game uses **Qwen2.5-14B** to understand natural language with human-like flexibility:

- **Natural Language Understanding**: Type commands naturally ("pick up the rusty dagger and head north" instead of "take dagger; go north")
- **Dynamic State Persistence**: Every action modifies a structured JSON game state that persists between sessions
- **Schema-Strict JSON Parsing**: LLM outputs are validated against a rigid schema, ensuring game integrity
- **Semantic World Engine**: The AI understands context, intent, and consequences without explicit programming for every scenario

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Player Input  │  "Attack the goblin with my sword"
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│         Ollama API (Qwen2.5-14B)            │
│  ┌───────────────────────────────────────┐  │
│  │  Prompt: Game State + Player Action  │  │
│  │  Output: Structured JSON Update      │  │
│  └───────────────────────────────────────┘  │
└────────┬────────────────────────────────────┘
         │ {player_actions: ["attack"], ...}
         ▼
┌─────────────────────────────────────────────┐
│          Game Engine (Python)               │
│  ┌───────────────────────────────────────┐  │
│  │  • Apply inventory changes            │  │
│  │  • Update player stats                │  │
│  │  • Modify NPC states                  │  │
│  │  • Track quest progress               │  │
│  └───────────────────────────────────────┘  │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  game_state.json│  → Persistent save file
└─────────────────┘
```

**Key Components:**
- **`main.py`**: Game loop, player I/O, and display formatting
- **`game_engine.py`**: State management and update application logic
- **`llm_parser.py`**: Ollama API interface and prompt construction
- **`game_data/`**: JSON files for initial and current game states

---

## 📋 Prerequisites

Before running this game, ensure you have:

1. **Python 3.9 or higher**
   ```bash
   python --version  # Should show 3.9.0 or higher
   ```

2. **Ollama** installed and running
   - Download from: [https://ollama.ai/](https://ollama.ai/)
   - Install the Qwen2.5-14B model:
     ```bash
     ollama pull qwen2.5:14b
     ```
   - Verify it's running:
     ```bash
     ollama list  # Should show qwen2.5:14b
     ```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd llm_rpg
```

### 2. Create a Virtual Environment
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Ollama Connection
```bash
# Make sure Ollama is running in the background
ollama list
```

### 5. Run the Game
```bash
python main.py
```

---

## 🎯 How to Play

### Starting the Game
When you launch `main.py`, you'll see:
```
============================================================
    🗡️  LLM-DRIVEN TEXT ADVENTURE RPG  🗡️
============================================================
Powered by Qwen2.5-14B Semantic World Engine
============================================================

📂 Loaded initial state from: game_data/initial_state.json
```

### Example Gameplay
```
📍 Location: Rusty Cave

You find yourself in a damp, musty cave. The walls are covered 
with orange rust-like formations...

🎒 Items here: old_map, rusty_dagger
🚪 Exits: north → forest_path

❤️  Health: 100 | 💰 Gold: 0 | ⭐ XP: 0
🎒 Inventory: Empty

------------------------------------------------------------

🎮 Your action (or 'quit' to exit): pick up the rusty dagger and examine the map

🤔 Interpreting your action...

✨ You: take_item, examine
📦 Gained: rusty_dagger

💭 You picked up the rusty dagger and studied the old map closely.
```

### Command Examples
- **Movement**: "go north", "head to the village", "enter the cave"
- **Interaction**: "take the sword", "talk to the merchant", "open the chest"
- **Combat**: "attack the goblin", "defend myself", "flee from danger"
- **Examination**: "look around", "examine the statue", "search for traps"
- **Mixed**: "grab the torch and go through the dark passage"

### Special Commands
- **`quit`** or **`exit`**: Save and exit the game
- **`help`** or **`?`**: Display help information
- **`stats`**: View detailed player statistics

---

## 🔑 Key Features

### 1. **Natural Language Understanding**
The game doesn't require memorizing commands. Just describe what you want to do naturally:
- ❌ Old way: `TAKE DAGGER` → `N` → `ATTACK GOBLIN`
- ✅ New way: "I'll grab that rusty dagger and head north to confront the goblin"

### 2. **Dynamic State Persistence**
Every action is saved automatically:
```json
{
  "player": {
    "location_id": "forest_path",
    "inventory": ["rusty_dagger", "old_map"],
    "health": 95,
    "gold": 10,
    "xp": 25
  }
}
```

### 3. **Schema-Strict JSON Parsing**
The LLM's responses are validated against a rigid structure, ensuring:
- No hallucinated items appear in your inventory
- Stats changes are calculated correctly
- Game state remains consistent

### 4. **Rich Game World**
Explore multiple locations with:
- **6+ unique areas**: caves, forests, villages, forges, inns
- **NPCs**: Talk to merchants, blacksmiths, bards, and mysterious travelers
- **Quests**: Track objectives and progress
- **Combat & Loot**: Fight enemies, collect items, gain experience

---

## 📁 Project Structure

```
llm_rpg/
├── main.py                      # Main game loop and display
├── game_engine.py               # State management and update logic
├── llm_parser.py                # Ollama API communication
├── game_data/
│   ├── initial_state.json       # Starting game world
│   └── current_state.json       # Auto-saved progress (gitignored)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
└── .gitignore                   # Git exclusions
```

---

## 🛠️ Technical Details

### LLM Prompt Engineering
The system uses a carefully crafted prompt that:
1. Provides the current game state as context
2. Defines a strict JSON schema for responses
3. Instructs the model to interpret player intent
4. Returns structured updates (no narrative prose)

### Update Schema
Every action generates a JSON object with these keys:
```json
{
  "player_actions": ["move", "take_item"],
  "inventory_changes": {
    "added": ["rusty_dagger"],
    "removed": []
  },
  "location_changes": {
    "new_location_id": "forest_path",
    "direction_moved": "north"
  },
  "player_stats_changes": {
    "health_change": 0,
    "gold_change": 0,
    "xp_gained": 5
  },
  "entity_interactions": [],
  "quest_updates": [],
  "game_events": [],
  "narrative_hint": "You ventured north into the forest."
}
```

### Error Handling
- **Ollama Connection Issues**: Gracefully degrades with error messages
- **JSON Parsing Failures**: Retries or skips malformed responses
- **State Corruption**: Loads initial state if save file is corrupted

---

## 🐛 Troubleshooting

### "Error communicating with Ollama"
**Solution**: Make sure Ollama is running:
```bash
# Start Ollama service
ollama serve
```

### "Model not found: qwen2.5:14b"
**Solution**: Pull the model first:
```bash
ollama pull qwen2.5:14b
```

### Game runs slowly
**Solution**: 
- Qwen2.5-14B requires significant compute resources
- Consider using a smaller model like `qwen2.5:7b` (edit `llm_parser.py`)
- Ensure your system has adequate RAM (16GB+ recommended)

### JSON parsing errors
**Solution**:
- This occasionally happens with LLMs
- The game will display an error and let you retry
- If persistent, check your Ollama version: `ollama --version`

---

## 🔮 Future Enhancements

Potential additions to make this even better:
- [ ] **Procedural World Generation**: Use LLM to create new locations dynamically
- [ ] **Voice Input**: Integrate speech-to-text for hands-free play
- [ ] **Multi-model Support**: Add Claude, GPT-4, or other LLM backends
- [ ] **Save Slots**: Multiple save files with named slots
- [ ] **Combat System**: Dice-rolling mechanics and strategic combat
- [ ] **Character Creation**: Choose race, class, starting stats
- [ ] **Multiplayer**: Connect multiple players in the same world

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ollama Team**: For providing an excellent local LLM runtime
- **Alibaba Cloud**: For developing the Qwen2.5 model family
- **Python Community**: For the amazing ecosystem of tools

---

## 💬 Contributing

Contributions are welcome! Feel free to:
- Report bugs via GitHub Issues
- Submit pull requests with improvements
- Share your game experiences and ideas

---

## 📧 Contact

Questions or suggestions? Open an issue on GitHub or reach out to the maintainer.

---

**Ready to embark on your AI-powered adventure? Run `python main.py` and let the journey begin!** 🗡️✨
