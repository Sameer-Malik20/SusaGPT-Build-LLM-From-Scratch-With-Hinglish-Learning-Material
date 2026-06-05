# GST LLM — Text Generation Entry Point
# Run: python generate.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.generate import main

if __name__ == "__main__":
    main()
