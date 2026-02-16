#!/usr/bin/env python3
"""
Setup and Verification Script for LLM-Driven Text Adventure RPG

Run this script to verify your environment is properly configured
before starting the game.
"""

import sys
import subprocess
import os


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_status(check_name, passed, message=""):
    """Print status of a check."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {check_name}")
    if message:
        print(f"     {message}")


def check_python_version():
    """Check if Python version is 3.9+."""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 9
    message = f"Python {version.major}.{version.minor}.{version.micro}"
    if not passed:
        message += " (Need Python 3.9+)"
    return passed, message


def check_ollama_installed():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(
            ['ollama', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        version = result.stdout.strip()
        return True, f"Ollama found: {version}"
    except FileNotFoundError:
        return False, "Ollama not found. Install from https://ollama.ai/"
    except subprocess.TimeoutExpired:
        return False, "Ollama command timed out"
    except Exception as e:
        return False, f"Error checking Ollama: {e}"


def check_qwen_model():
    """Check if Qwen2.5-14B model is available."""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        models = result.stdout.lower()
        has_14b = 'qwen2.5:14b' in models
        has_7b = 'qwen2.5:7b' in models or 'qwen2.5' in models
        
        if has_14b:
            return True, "qwen2.5:14b found"
        elif has_7b:
            return False, "Found other Qwen model. Run: ollama pull qwen2.5:14b"
        else:
            return False, "No Qwen model found. Run: ollama pull qwen2.5:14b"
    except FileNotFoundError:
        return False, "Cannot check models (Ollama not found)"
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, f"Error checking models: {e}"


def check_dependencies():
    """Check if required Python packages are installed."""
    try:
        import ollama
        return True, "ollama package installed"
    except ImportError:
        return False, "Run: pip install -r requirements.txt"


def check_game_files():
    """Check if essential game files exist."""
    essential_files = [
        'main.py',
        'game_engine.py',
        'llm_parser.py',
        'game_data/initial_state.json',
        'requirements.txt'
    ]
    
    missing = []
    for file in essential_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    return True, "All essential files present"


def main():
    """Run all checks."""
    print_header("🗡️  LLM-RPG Environment Verification")
    
    checks = [
        ("Python Version", check_python_version),
        ("Ollama Installation", check_ollama_installed),
        ("Qwen2.5-14B Model", check_qwen_model),
        ("Python Dependencies", check_dependencies),
        ("Game Files", check_game_files)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        passed, message = check_func()
        print_status(check_name, passed, message)
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to play!")
        print("\nTo start the game, run:")
        print("    python main.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nQuick Setup Guide:")
        print("  1. Install Ollama: https://ollama.ai/")
        print("  2. Pull model: ollama pull qwen2.5:14b")
        print("  3. Install deps: pip install -r requirements.txt")
    
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
