import os
import importlib
import traceback
from fastapi import APIRouter
import json

# Define the global plugin router to be mounted on the main FastAPI app
plugin_router = APIRouter(prefix="/plugins", tags=["Extensions"])

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.active_plugins = {}
        
    def _validate_signature(self, plugin_name: str) -> bool:
        """
        Mock security validation. In production, this verifies Ed25519 signatures
        to ensure third-party code hasn't been tampered with.
        """
        # Hardcoded to True for development
        return True

    def load_all_plugins(self):
        """
        Dynamically scans the /plugins directory and safely mounts 
        any valid plugins without crashing the main server.
        """
        print("=== ApisLM Plugin Manager: Initializing Extension Scan ===")
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]
                self.load_plugin(plugin_name)

    def load_plugin(self, plugin_name: str):
        """
        Dynamically imports a single plugin module.
        Sandboxing logic: Wraps import in try/except so a bad plugin 
        never crashes the core Swarm Intelligence engine.
        """
        try:
            if not self._validate_signature(plugin_name):
                print(f"[SECURITY] Plugin '{plugin_name}' failed signature validation. Skipping.")
                return

            print(f"Mounting Extension: {plugin_name}...")
            
            # Dynamic import
            module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")
            
            # Hook execution (Look for a setup() function)
            if hasattr(module, 'setup'):
                # Pass the global router so plugins can register endpoints safely
                module.setup(plugin_router)
                self.active_plugins[plugin_name] = module
                print(f"[OK] {plugin_name} successfully loaded.")
            else:
                print(f"[WARN] {plugin_name} has no setup(router) function. Ignored.")
                
        except Exception as e:
            # Crucial: Graceful error handling for third-party code
            print(f"❌ [ERROR] Failed to load plugin '{plugin_name}'. Main server is unaffected.")
            print(f"Exception: {e}")
            # traceback.print_exc()

# Singleton instance to be imported by main_api.py
manager = PluginManager()

if __name__ == "__main__":
    # Test execution
    manager.load_all_plugins()
    print(f"Active Extensions: {list(manager.active_plugins.keys())}")
