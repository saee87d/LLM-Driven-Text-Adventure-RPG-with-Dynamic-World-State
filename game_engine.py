"""
Game Engine Module

Manages game state, applies updates from the LLM parser,
and handles loading/saving to JSON files.
"""

import json
import os
from typing import Dict, Any, Optional
from copy import deepcopy


class GameEngine:
    """
    Core game engine responsible for managing world state.
    
    Attributes:
        game_state (dict): Current complete game state
        game_data_dir (str): Path to game data directory
        current_state_file (str): Path to current save file
        initial_state_file (str): Path to initial state template
    """
    
    def __init__(self, game_data_dir: str = "game_data"):
        """
        Initialize the game engine.
        
        Args:
            game_data_dir (str): Directory containing game data files
        """
        self.game_data_dir = game_data_dir
        self.current_state_file = os.path.join(game_data_dir, "current_state.json")
        self.initial_state_file = os.path.join(game_data_dir, "initial_state.json")
        self.game_state: Dict[str, Any] = {}
    
    def load_state(self) -> bool:
        """
        Load game state from current_state.json, or initial_state.json if not found.
        
        Returns:
            bool: True if load successful, False otherwise
        """
        # Try loading current state first
        if os.path.exists(self.current_state_file):
            try:
                with open(self.current_state_file, 'r', encoding='utf-8') as f:
                    self.game_state = json.load(f)
                print(f"📂 Loaded save from: {self.current_state_file}")
                return True
            except json.JSONDecodeError as e:
                print(f"⚠️  Corrupted save file: {e}")
                print("Loading initial state instead...")
        
        # Load initial state
        if os.path.exists(self.initial_state_file):
            try:
                with open(self.initial_state_file, 'r', encoding='utf-8') as f:
                    self.game_state = json.load(f)
                print(f"📂 Loaded initial state from: {self.initial_state_file}")
                # Save as current state
                self.save_state()
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Error loading initial state: {e}")
                return False
        
        print("❌ No game state files found!")
        return False
    
    def save_state(self) -> bool:
        """
        Save current game state to current_state.json.
        
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(self.game_data_dir, exist_ok=True)
            
            # Write to file with pretty formatting
            with open(self.current_state_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_state, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Error saving game state: {e}")
            return False
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get a copy of the current game state.
        
        Returns:
            dict: Deep copy of game state
        """
        return deepcopy(self.game_state)
    
    def apply_update(self, update_data: Dict[str, Any]) -> bool:
        """
        Apply structured update from LLM parser to game state.
        
        Args:
            update_data (dict): Structured update containing changes
        
        Returns:
            bool: True if update applied successfully
        """
        try:
            # Ensure player exists
            if 'player' not in self.game_state:
                self.game_state['player'] = {
                    'location_id': 'start',
                    'inventory': [],
                    'health': 100,
                    'gold': 0,
                    'xp': 0
                }
            
            player = self.game_state['player']
            
            # Apply inventory changes
            self._apply_inventory_changes(update_data.get('inventory_changes', {}))
            
            # Apply location changes
            self._apply_location_changes(update_data.get('location_changes', {}))
            
            # Apply player stats changes
            self._apply_stats_changes(update_data.get('player_stats_changes', {}))
            
            # Apply room state updates
            self._apply_room_updates(update_data.get('location_changes', {}).get('room_state_updates', []))
            
            # Apply entity interactions
            self._apply_entity_interactions(update_data.get('entity_interactions', []))
            
            # Apply quest updates
            self._apply_quest_updates(update_data.get('quest_updates', []))
            
            # Process game events
            self._process_game_events(update_data.get('game_events', []))
            
            return True
        
        except Exception as e:
            print(f"❌ Error applying update: {e}")
            return False
    
    def _apply_inventory_changes(self, changes: Dict[str, list]) -> None:
        """
        Apply inventory changes to player.
        
        Args:
            changes (dict): Inventory change data
        """
        player = self.game_state['player']
        inventory = player.get('inventory', [])
        
        # Add items
        for item in changes.get('added', []):
            if item not in inventory:
                inventory.append(item)
        
        # Remove items
        for item in changes.get('removed', []):
            if item in inventory:
                inventory.remove(item)
        
        # Handle equipped/unequipped (for future use)
        if 'equipped' in changes:
            player['equipped'] = player.get('equipped', []) + changes['equipped']
        
        if 'unequipped' in changes:
            equipped = player.get('equipped', [])
            for item in changes['unequipped']:
                if item in equipped:
                    equipped.remove(item)
        
        player['inventory'] = inventory
    
    def _apply_location_changes(self, changes: Dict[str, Any]) -> None:
        """
        Apply location changes (player movement).
        
        Args:
            changes (dict): Location change data
        """
        new_location = changes.get('new_location_id')
        if new_location:
            self.game_state['player']['location_id'] = new_location
    
    def _apply_stats_changes(self, changes: Dict[str, int]) -> None:
        """
        Apply player stat changes.
        
        Args:
            changes (dict): Stat change data
        """
        player = self.game_state['player']
        
        # Apply health change
        health_change = changes.get('health_change', 0)
        if health_change != 0:
            player['health'] = max(0, player.get('health', 100) + health_change)
        
        # Apply mana change (if using mana)
        mana_change = changes.get('mana_change', 0)
        if mana_change != 0:
            player['mana'] = max(0, player.get('mana', 0) + mana_change)
        
        # Apply gold change
        gold_change = changes.get('gold_change', 0)
        if gold_change != 0:
            player['gold'] = max(0, player.get('gold', 0) + gold_change)
        
        # Apply XP gain
        xp_gained = changes.get('xp_gained', 0)
        if xp_gained > 0:
            player['xp'] = player.get('xp', 0) + xp_gained
    
    def _apply_room_updates(self, updates: list) -> None:
        """
        Apply updates to room objects/features.
        
        Args:
            updates (list): List of room state updates
        """
        player_location = self.game_state['player'].get('location_id')
        locations = self.game_state.get('locations', {})
        
        if player_location not in locations:
            return
        
        current_room = locations[player_location]
        
        for update in updates:
            object_id = update.get('object_id')
            new_state = update.get('state')
            
            # Store object states in room metadata
            if 'object_states' not in current_room:
                current_room['object_states'] = {}
            
            current_room['object_states'][object_id] = new_state
            
            # If state is "missing", remove from items_present
            if new_state == "missing" and object_id in current_room.get('items_present', []):
                current_room['items_present'].remove(object_id)
    
    def _apply_entity_interactions(self, interactions: list) -> None:
        """
        Apply entity interactions (NPC, monster, object interactions).
        
        Args:
            interactions (list): List of entity interactions
        """
        npcs = self.game_state.get('npcs', {})
        
        for interaction in interactions:
            entity_id = interaction.get('id')
            entity_type = interaction.get('type')
            action = interaction.get('action')
            outcome = interaction.get('outcome')
            
            # Handle NPC interactions
            if entity_type == 'NPC' and entity_id in npcs:
                npc = npcs[entity_id]
                
                # Update NPC based on interaction
                if action == 'attacked':
                    if 'health' in npc:
                        npc['health'] = max(0, npc.get('health', 100) - 10)
                    npc['hostile'] = True
                
                elif action == 'talked_to':
                    npc['talked'] = True
                
                # If outcome indicates death/removal
                if outcome in ['killed', 'defeated', 'destroyed']:
                    npc['alive'] = False
                    # Remove from location
                    player_location = self.game_state['player'].get('location_id')
                    if player_location in self.game_state.get('locations', {}):
                        npcs_present = self.game_state['locations'][player_location].get('npcs_present', [])
                        if entity_id in npcs_present:
                            npcs_present.remove(entity_id)
    
    def _apply_quest_updates(self, updates: list) -> None:
        """
        Apply quest status updates.
        
        Args:
            updates (list): List of quest updates
        """
        if 'quests' not in self.game_state:
            self.game_state['quests'] = {}
        
        quests = self.game_state['quests']
        
        for update in updates:
            quest_id = update.get('quest_id')
            status = update.get('status')
            
            # Create quest if doesn't exist
            if quest_id not in quests:
                quests[quest_id] = {
                    'status': 'not_started',
                    'objectives': []
                }
            
            # Update quest status
            if status == 'started':
                quests[quest_id]['status'] = 'in_progress'
            elif status in ['completed', 'failed']:
                quests[quest_id]['status'] = status
            
            # Handle objective updates
            objective_id = update.get('objective_id')
            if objective_id:
                if 'completed_objectives' not in quests[quest_id]:
                    quests[quest_id]['completed_objectives'] = []
                
                if objective_id not in quests[quest_id]['completed_objectives']:
                    quests[quest_id]['completed_objectives'].append(objective_id)
    
    def _process_game_events(self, events: list) -> None:
        """
        Process special game events.
        
        Args:
            events (list): List of game events
        """
        # Store events in game history
        if 'event_history' not in self.game_state:
            self.game_state['event_history'] = []
        
        self.game_state['event_history'].extend(events)
        
        # Limit history size
        if len(self.game_state['event_history']) > 100:
            self.game_state['event_history'] = self.game_state['event_history'][-100:]
