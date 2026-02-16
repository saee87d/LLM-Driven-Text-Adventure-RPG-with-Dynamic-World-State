"""
LLM Parser Module

Handles communication with Ollama (Qwen2.5-14B) for parsing
player natural language input into structured JSON updates.
"""

import json
from typing import Dict, Any
import ollama


class LLMParser:
    """
    Parser that uses Qwen2.5-14B via Ollama to interpret player actions.
    
    Attributes:
        model_name (str): Name of the Ollama model to use
        temperature (float): Temperature for generation (0.0 for deterministic)
    """
    
    def __init__(self, model_name: str = "qwen2.5:14b", temperature: float = 0.0):
        """
        Initialize the LLM parser.
        
        Args:
            model_name (str): Ollama model identifier
            temperature (float): Generation temperature
        """
        self.model_name = model_name
        self.temperature = temperature
    
    def parse_player_action(self, player_input: str, current_game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse player's natural language action into structured JSON.
        
        Args:
            player_input (str): Player's text input
            current_game_state (dict): Current game world state
        
        Returns:
            dict: Structured update data or error information
        """
        try:
            # Construct the prompt
            prompt = self._build_prompt(player_input, current_game_state)
            
            # Call Ollama API
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                format='json',
                options={
                    'temperature': self.temperature,
                    'num_predict': 1000  # Max tokens for response
                }
            )
            
            # Extract response text
            response_text = response.get('response', '').strip()
            
            if not response_text:
                return self._create_error_response("Empty response from LLM")
            
            # Parse JSON
            try:
                update_data = json.loads(response_text)
                
                # Validate structure
                if not isinstance(update_data, dict):
                    return self._create_error_response("LLM response is not a JSON object")
                
                # Ensure all required keys exist (with defaults)
                update_data = self._normalize_update_data(update_data)
                
                return update_data
            
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON parse error: {e}")
                print(f"Raw response: {response_text[:200]}...")
                return self._create_error_response(f"Invalid JSON from LLM: {str(e)}")
        
        except Exception as e:
            print(f"❌ Error communicating with Ollama: {e}")
            return self._create_error_response(f"LLM communication error: {str(e)}")
    
    def _build_prompt(self, player_input: str, game_state: Dict[str, Any]) -> str:
        """
        Build the comprehensive prompt for the LLM.
        
        Args:
            player_input (str): Player's action
            game_state (dict): Current game state
        
        Returns:
            str: Complete prompt for LLM
        """
        # Convert game state to JSON string
        game_state_json = json.dumps(game_state, indent=2, ensure_ascii=False)
        
        prompt = f"""You are the Game Master for a text-based adventure RPG. Your primary role is to interpret player actions and translate them into structured JSON data that updates the game's state.

**Current Game State (for context, do not modify directly unless requested):**
```json
{game_state_json}
```

**Instructions:**

1. Analyze the Player's Action: Understand the player's intent, specific objects they interact with, their movement, combat actions, or dialogue.

2. Generate JSON Output ONLY: Your response MUST be a valid JSON object. Do not include any conversational text, explanations, or narrative.

3. JSON Structure: The JSON object MUST contain the following top-level keys. If a key is not relevant to the player's action, its value should be an empty array or an empty object, or null if it's a single value.

   - **player_actions**: (array of strings) A summary of the distinct actions the player performed (e.g., "move", "take_item", "attack", "talk", "use_item", "examine").
   
   - **inventory_changes**: (object)
     - added: (array of strings) List of item IDs or names added to player's inventory.
     - removed: (array of strings) List of item IDs or names removed from player's inventory.
     - equipped: (array of strings) List of item IDs or names newly equipped by the player.
     - unequipped: (array of strings) List of item IDs or names unequipped by the player.
   
   - **entity_interactions**: (array of objects) Details about interactions with NPCs or other dynamic entities.
     - id: (string) Identifier of the entity (e.g., "goblin_01", "old_merchant").
     - type: (string) Type of entity (e.g., "NPC", "monster", "door").
     - action: (string) What the player did to or with it (e.g., "attacked", "talked_to", "opened").
     - outcome: (string, optional) Result of the interaction (e.g., "damaged", "opened", "angered").
   
   - **location_changes**: (object)
     - new_location_id: (string or null) The ID of the new room/area if the player moved.
     - direction_moved: (string or null) "north", "south", "east", "west", "up", "down", "enter", "exit" if relevant.
     - room_state_updates: (array of objects) Changes to the current room's objects/features.
       - object_id: (string) ID of the object (e.g., "treasure_chest", "lever").
       - state: (string) New state (e.g., "opened", "activated", "broken", "missing").
   
   - **player_stats_changes**: (object)
     - health_change: (integer, can be negative) Change in player's health.
     - mana_change: (integer, can be negative) Change in player's mana/energy.
     - gold_change: (integer, can be negative) Change in player's gold.
     - xp_gained: (integer) Experience points gained.
   
   - **quest_updates**: (array of objects)
     - quest_id: (string) ID of the quest.
     - status: (string) New status ("started", "completed", "failed", "updated_objective").
     - objective_id: (string, optional) If only a specific objective within a quest was updated.
   
   - **game_events**: (array of strings) Any special events triggered (e.g., "trap_sprung", "secret_revealed", "new_NPC_spawned").
   
   - **narrative_hint**: (string or null) A brief, objective hint about what happened or changed in the world, not a full narrative description. This helps the game engine know what to describe next.

Now, interpret the following player action:

**Player**: "{player_input}"

Return ONLY valid JSON with no additional text:"""
        
        return prompt
    
    def _normalize_update_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure all expected keys exist in update data with proper defaults.
        
        Args:
            data (dict): Raw update data from LLM
        
        Returns:
            dict: Normalized update data
        """
        normalized = {
            'player_actions': data.get('player_actions', []),
            'inventory_changes': {
                'added': [],
                'removed': [],
                'equipped': [],
                'unequipped': []
            },
            'entity_interactions': data.get('entity_interactions', []),
            'location_changes': {
                'new_location_id': None,
                'direction_moved': None,
                'room_state_updates': []
            },
            'player_stats_changes': {
                'health_change': 0,
                'mana_change': 0,
                'gold_change': 0,
                'xp_gained': 0
            },
            'quest_updates': data.get('quest_updates', []),
            'game_events': data.get('game_events', []),
            'narrative_hint': data.get('narrative_hint', None)
        }
        
        # Merge inventory changes
        if 'inventory_changes' in data:
            inv = data['inventory_changes']
            normalized['inventory_changes']['added'] = inv.get('added', [])
            normalized['inventory_changes']['removed'] = inv.get('removed', [])
            normalized['inventory_changes']['equipped'] = inv.get('equipped', [])
            normalized['inventory_changes']['unequipped'] = inv.get('unequipped', [])
        
        # Merge location changes
        if 'location_changes' in data:
            loc = data['location_changes']
            normalized['location_changes']['new_location_id'] = loc.get('new_location_id')
            normalized['location_changes']['direction_moved'] = loc.get('direction_moved')
            normalized['location_changes']['room_state_updates'] = loc.get('room_state_updates', [])
        
        # Merge stats changes
        if 'player_stats_changes' in data:
            stats = data['player_stats_changes']
            normalized['player_stats_changes']['health_change'] = stats.get('health_change', 0)
            normalized['player_stats_changes']['mana_change'] = stats.get('mana_change', 0)
            normalized['player_stats_changes']['gold_change'] = stats.get('gold_change', 0)
            normalized['player_stats_changes']['xp_gained'] = stats.get('xp_gained', 0)
        
        return normalized
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """
        Create a standardized error response.
        
        Args:
            error_message (str): Description of the error
        
        Returns:
            dict: Error response with empty update structure
        """
        return {
            'error': error_message,
            'player_actions': [],
            'inventory_changes': {
                'added': [],
                'removed': [],
                'equipped': [],
                'unequipped': []
            },
            'entity_interactions': [],
            'location_changes': {
                'new_location_id': None,
                'direction_moved': None,
                'room_state_updates': []
            },
            'player_stats_changes': {
                'health_change': 0,
                'mana_change': 0,
                'gold_change': 0,
                'xp_gained': 0
            },
            'quest_updates': [],
            'game_events': [],
            'narrative_hint': None
        }
