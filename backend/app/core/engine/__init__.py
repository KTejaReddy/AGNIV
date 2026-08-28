from .event_bus import event_bus, Event
from .input_manager import input_manager, InputType
from .action_planner import action_planner
from .capability_manager import capability_manager
from .permission_manager import permission_manager
from .task_manager import task_manager
from .context_manager import context_manager
from .session_manager import session_manager
from .diagnostics_engine import diagnostics_engine

async def initialize_engine(ws_manager):
    event_bus.set_ws_manager(ws_manager)
    await event_bus.start()
    
    await action_planner.initialize()
    await capability_manager.initialize()
    await permission_manager.initialize()
    await task_manager.initialize()
    await context_manager.initialize()
    await session_manager.initialize()
    await diagnostics_engine.initialize()
