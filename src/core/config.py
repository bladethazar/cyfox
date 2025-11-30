"""Configuration management"""
import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class Config:
    """Configuration manager"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # Default to config/config.yaml relative to project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from YAML file"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            print(f"Warning: Config file not found at {self.config_path}, using defaults")
            self._config = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'display.width')"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def save(self):
        """Save configuration to YAML file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, default_flow_style=False, sort_keys=False)

