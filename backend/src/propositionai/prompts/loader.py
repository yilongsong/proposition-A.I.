import os
import yaml
from string import Template

class PromptLoader:
    """Loads and manages prompts from YAML files."""
    
    def __init__(self, prompts_dir=None):
        if prompts_dir is None:
            prompts_dir = os.path.dirname(os.path.abspath(__file__))
        self.prompts_dir = prompts_dir
        self.prompts = {}
        self._load_prompts()
    
    def _load_prompts(self):
        """Recursively load all YAML files from prompts directory."""
        for root, _, files in os.walk(self.prompts_dir):
            for file in files:
                if file.endswith('.yaml'):
                    path = os.path.join(root, file)
                    name = os.path.splitext(os.path.relpath(path, self.prompts_dir))[0]
                    with open(path, 'r') as f:
                        self.prompts[name] = yaml.safe_load(f)
    
    def get_prompt(self, name: str, **kwargs) -> str:
        """Get a prompt by name and format it with provided kwargs."""
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found")
        
        template = Template(self.prompts[name]['template'])
        return template.safe_substitute(**kwargs)