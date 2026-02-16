#!/usr/bin/env python3
"""
LLM-Driven Text Adventure RPG - Main Game Loop

This module handles the primary game loop, player input/output,
and coordinates between the game engine and LLM parser.
"""

import sys
from game_engine import GameEngine
from llm_parser import LLMParser


class GameDisplay:
    """Handles all game display output with formatting."""
    
    @staticmethod
    def print_header():
        """Print the game header."""
        print("\n" + "=" * 60)
        print("    🗡️  LLM-DRIVEN TEXT ADVENTURE RPG  🗡️")
        print("=" * 60)
        print("Powered by Qwen2.5-14B Semantic World Engine")
        print("=" * 60 + "\n")
    
    @staticmethod
    def print_separator():
        """Print a visual separator."""
        print("\n" + "-" * 60 + "\n")
    
    @staticmethod
    def print_location(location_data, location_id):
        """
        Display current location details.
        
        Args:
            location_data (dict): Location information
            location_id (str): Current location identifier
        """
        print(f"\n📍 Location: {location_id.replace('_', ' ').title()}")
        print(f"\n{location_data.get('description', 'A mysterious place.')}")
        
        # Display items
        items = location_data.get('items_present', [])
        if items:
            print(f"\n🎒 Items here: {', '.join(items)}")
        
        # Display NPCs
        npcs = location_data.get('npcs_present', [])
        if npcs:
            print(f"\n👥 NPCs present: {', '.join(npcs)}")
        
        # Display exits
        exits = location_data.get('exits', {})
        if exits:
            exit_list = [f"{direction} → {dest}" for direction, dest in exits.items()]
            print(f"\n🚪 Exits: {', '.join(exit_list)}")
    
    @staticmethod
    def print_player_stats(player_data):
        """
        Display player statistics.
        
        Args:
            player_data (dict): Player information
        """
        print(f"\n❤️  Health: {player_data.get('health', 100)} | "
              f"💰 Gold: {player_data.get('gold', 0)} | "
              f"⭐ XP: {player_data.get('xp', 0)}")
        
        inventory = player_data.get('inventory', [])
        if inventory:
            print(f"🎒 Inventory: {', '.join(inventory)}")
        else:
            print("🎒 Inventory: Empty")
    
    @staticmethod
    def print_update_feedback(update_data):
        """
        Display feedback about what happened during the turn.
        
        Args:
            update_data (dict): Update information from LLM parser
        """
        # Player actions
        actions = update_data.get('player_actions', [])
        if actions:
            print(f"\n✨ You: {', '.join(actions)}")
        
        # Inventory changes
        inv_changes = update_data.get('inventory_changes', {})
        added = inv_changes.get('added', [])
        removed = inv_changes.get('removed', [])
        
        if added:
            print(f"📦 Gained: {', '.join(added)}")
        if removed:
            print(f"📤 Lost: {', '.join(removed)}")
        
        # Entity interactions
        interactions = update_data.get('entity_interactions', [])
        for interaction in interactions:
            entity_id = interaction.get('id', 'something')
            action = interaction.get('action', 'interacted with')
            outcome = interaction.get('outcome', '')
            
            msg = f"⚔️  {action.replace('_', ' ').capitalize()} {entity_id}"
            if outcome:
                msg += f" - {outcome}"
            print(msg)
        
        # Stats changes
        stats = update_data.get('player_stats_changes', {})
        if stats.get('health_change', 0) != 0:
            change = stats['health_change']
            symbol = "+" if change > 0 else ""
            print(f"❤️  Health {symbol}{change}")
        
        if stats.get('gold_change', 0) != 0:
            change = stats['gold_change']
            symbol = "+" if change > 0 else ""
            print(f"💰 Gold {symbol}{change}")
        
        if stats.get('xp_gained', 0) > 0:
            print(f"⭐ XP +{stats['xp_gained']}")
        
        # Quest updates
        quests = update_data.get('quest_updates', [])
        for quest in quests:
            quest_id = quest.get('quest_id', 'Unknown')
            status = quest.get('status', 'updated')
            print(f"📜 Quest '{quest_id}': {status}")
        
        # Game events
        events = update_data.get('game_events', [])
        for event in events:
            print(f"⚡ {event.replace('_', ' ').capitalize()}!")
        
        # Narrative hint
        hint = update_data.get('narrative_hint')
        if hint:
            print(f"\n💭 {hint}")


def main():
    """Main game loop."""
    # Initialize components
    display = GameDisplay()
    engine = GameEngine()
    parser = LLMParser()
    
    # Display welcome
    display.print_header()
    
    # Load game state
    try:
        engine.load_state()
        print("✅ Game loaded successfully!")
    except Exception as e:
        print(f"⚠️  Error loading game: {e}")
        print("Starting new game...")
    
    # Main game loop
    running = True
    first_turn = True
    
    while running:
        try:
            display.print_separator()
            
            # Get current game state
            state = engine.get_state()
            player = state.get('player', {})
            location_id = player.get('location_id', 'unknown')
            locations = state.get('locations', {})
            current_location = locations.get(location_id, {})
            
            # Display current state
            if first_turn or location_id:
                display.print_location(current_location, location_id)
                display.print_player_stats(player)
                first_turn = False
            
            display.print_separator()
            
            # Get player input
            player_input = input("🎮 Your action (or 'quit' to exit): ").strip()
            
            # Handle quit
            if player_input.lower() in ['quit', 'exit', 'q']:
                print("\n💾 Saving game...")
                engine.save_state()
                print("👋 Thanks for playing! Goodbye!")
                running = False
                continue
            
            # Handle empty input
            if not player_input:
                print("⚠️  Please enter an action.")
                continue
            
            # Handle special commands
            if player_input.lower() in ['help', '?']:
                print("\n📖 Help:")
                print("  - Describe your actions naturally (e.g., 'go north', 'take dagger')")
                print("  - Talk to NPCs, examine items, fight enemies")
                print("  - Type 'quit' to save and exit")
                print("  - Type 'stats' to see detailed player info")
                continue
            
            if player_input.lower() == 'stats':
                display.print_player_stats(player)
                continue
            
            # Parse action with LLM
            print("\n🤔 Interpreting your action...")
            update_data = parser.parse_player_action(player_input, state)
            
            # Check for parsing errors
            if update_data.get('error'):
                print(f"❌ Error: {update_data['error']}")
                print("💡 Try rephrasing your action or type 'help' for guidance.")
                continue
            
            # Apply update to game state
            success = engine.apply_update(update_data)
            
            if success:
                # Display feedback
                display.print_update_feedback(update_data)
                
                # Auto-save after each turn
                engine.save_state()
            else:
                print("⚠️  Could not apply update. Game state unchanged.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Game interrupted. Saving...")
            engine.save_state()
            print("👋 Goodbye!")
            running = False
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("💾 Attempting to save game state...")
            try:
                engine.save_state()
            except:
                pass
            print("Game continues...")


if __name__ == "__main__":
    main()
