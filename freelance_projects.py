import os
from app import run

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    run(config_path=config_path)
