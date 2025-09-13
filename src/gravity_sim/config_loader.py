from dataclasses import dataclass
import re

@dataclass
class Config:
    """Dataclass to store the starting config of a simulation."""
    


class ConfigLoader:
    """Loads simulation configs from various types of config files."""
    
    @staticmethod
    def load_file(filename: str) -> Config:
        if re.search(".*.y*ml", filename):
            return ConfigLoader.from_yaml(filename)
    
    @staticmethod
    def from_yaml(filename: str):
        pass
    
    @staticmethod
    def from_json() -> Config:
        pass