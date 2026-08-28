import os
import importlib
from app.core.logging import logger

PLUGINS_DIR = "plugins"

if not os.path.exists(PLUGINS_DIR):
    os.makedirs(PLUGINS_DIR)

class PluginLoader:
    def __init__(self):
        self.plugins = {}
        
    def discover_plugins(self):
        discovered = []
        for item in os.listdir(PLUGINS_DIR):
            if os.path.isdir(os.path.join(PLUGINS_DIR, item)):
                if not item.startswith("__"):
                    discovered.append(item)
        return discovered

    def register_plugin(self, plugin_name: str):
        try:
            module = importlib.import_module(f"{PLUGINS_DIR}.{plugin_name}.main")
            if hasattr(module, "Plugin"):
                self.plugins[plugin_name] = module.Plugin()
                logger.info(f"Registered plugin: {plugin_name}")
                return True
            else:
                logger.error(f"Plugin {plugin_name} missing Plugin class")
                return False
        except Exception as e:
            logger.error(f"Error registering plugin {plugin_name}: {e}")
            return False

    def enable_plugin(self, plugin_name: str):
        if plugin_name in self.plugins:
            try:
                self.plugins[plugin_name].enable()
                logger.info(f"Enabled plugin: {plugin_name}")
                return True
            except Exception as e:
                logger.error(f"Error enabling plugin {plugin_name}: {e}")
        return False

    def disable_plugin(self, plugin_name: str):
        if plugin_name in self.plugins:
            try:
                self.plugins[plugin_name].disable()
                logger.info(f"Disabled plugin: {plugin_name}")
                return True
            except Exception as e:
                logger.error(f"Error disabling plugin {plugin_name}: {e}")
        return False

    def unload_plugin(self, plugin_name: str):
        if plugin_name in self.plugins:
            self.disable_plugin(plugin_name)
            del self.plugins[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        return False

    def get_metadata(self, plugin_name: str):
        if plugin_name in self.plugins:
            try:
                return self.plugins[plugin_name].metadata()
            except Exception as e:
                logger.error(f"Error fetching metadata for {plugin_name}: {e}")
        return {}

plugin_loader = PluginLoader()
