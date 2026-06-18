import os
from pathlib import Path
from dotenv import load_dotenv

def init_config():
    current = Path(__file__).resolve()
    
    for parent in current.parents:
        env_path = parent / ".env"
        if env_path.is_file():
            load_dotenv(dotenv_path=env_path)
            return True
            
    load_dotenv() 
    return False
