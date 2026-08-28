import asyncio
import websockets
import json
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text

console = Console()

class DiagnosticsState:
    def __init__(self):
        self.metrics = None
        self.connected = False
        
    def handle_event(self, event):
        etype = event.get("type", "")
        payload = event.get("payload", {})
        
        if etype == "DIAGNOSTICS_UPDATE":
            self.metrics = payload

state = DiagnosticsState()

def generate_ui():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=7)
    )
    
    layout["main"].split_row(
        Layout(name="subsystems", ratio=1),
        Layout(name="middle_col", ratio=1),
        Layout(name="right_col", ratio=1)
    )
    
    layout["middle_col"].split_column(
        Layout(name="pipeline", ratio=1),
        Layout(name="runtime_state", ratio=1)
    )
    
    if not state.connected:
        layout["header"].update(Panel("[bold red]DISCONNECTED[/bold red] - Waiting for backend...", title="AGNIV Runtime Diagnostics"))
        return layout
        
    if not state.metrics:
        layout["header"].update(Panel("[bold yellow]CONNECTED[/bold yellow] - Waiting for first update...", title="AGNIV Runtime Diagnostics"))
        return layout

    m = state.metrics
    subsystems = m.get("subsystems", {})
    runtime_state = m.get("runtime_state", {})
    pipeline = m.get("pipeline", {})
    failure = m.get("failure_inspector")
    events = m.get("recent_events", [])
    
    # Header
    score = m.get("health_score", 0)
    color = "green" if score == 100 else "yellow" if score > 50 else "red"
    header_text = f"Health Score: [bold {color}]{score}%[/bold {color}] | CPU: {m.get('cpu_percent')}% | RAM: {m.get('memory_percent')}% | Session: {runtime_state.get('session_uuid')}"
    layout["header"].update(Panel(header_text, title="AGNIV Runtime Diagnostics"))
    
    # Subsystems (Left Col)
    sys_table = Table(show_header=False, expand=True)
    sys_table.add_column("Subsystem")
    sys_table.add_column("Status", justify="right")
    
    for name, data in subsystems.items():
        sys_table.add_row(name, data["status"])
        
    layout["subsystems"].update(Panel(sys_table, title="Subsystems"))
    
    # Pipeline (Middle Top)
    active_stage = pipeline.get("active_stage", "None")
    stages = ["Wake Word", "Speech Recognition", "Transcript", "Groq", "Execution Plan", "Capability", "Desktop", "TTS", "Listening"]
    
    pipe_text = ""
    for s in stages:
        if s == active_stage:
            pipe_text += f"[bold green]> {s}[/bold green]\n"
        else:
            pipe_text += f"[dim]  {s}[/dim]\n"
            
    layout["pipeline"].update(Panel(pipe_text, title="Live Pipeline"))
    
    # Runtime State (Middle Bottom)
    rs_text = f"""[bold]Current Goal:[/bold] {runtime_state.get('current_goal')}
[bold]Current Workflow:[/bold] {runtime_state.get('current_workflow')}
[bold]Memory Context Size:[/bold] {runtime_state.get('current_memory_context_size')}
[bold]Conversation Length:[/bold] {runtime_state.get('conversation_length')}
[bold]TTS State:[/bold] {runtime_state.get('current_tts_state')}
[bold]STT State:[/bold] {runtime_state.get('current_stt_state')}
[bold]Planner State:[/bold] {runtime_state.get('current_planner_state')}
[bold]Runtime Engine:[/bold] {runtime_state.get('runtime_state_val')}
"""
    layout["runtime_state"].update(Panel(rs_text, title="Runtime State"))
    
    # Event Timeline (Right Col)
    events_text = ""
    for e in events[-20:]: # show last 20
        events_text += f"[{e.get('source', '?')}] {e.get('type')}\n"
    layout["right_col"].update(Panel(events_text, title="Event Timeline (Recent)"))
    
    # Footer (Failure Inspector)
    if failure:
        fail_text = f"[bold red]FAILURE IN {failure.get('feature')}[/bold red]\n"
        fail_text += f"Reason: {failure.get('failure')}\n"
        fail_text += f"Root Cause: {failure.get('root_cause')}\n"
        fail_text += f"Location: {failure.get('file')}::{failure.get('function')}\n"
        fail_text += f"[bold yellow]Suggested Fix:[/bold yellow] {failure.get('suggested_fix')}"
        layout["footer"].update(Panel(fail_text, title="Failure Inspector", border_style="red"))
    else:
        layout["footer"].update(Panel("[green]All systems operational.[/green]", title="Failure Inspector"))
    
    return layout

async def listen_to_ws():
    uri = "ws://localhost:8000/ws"
    while True:
        try:
            async with websockets.connect(uri) as ws:
                state.connected = True
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    if data.get("type") == "CORE_EVENT":
                        state.handle_event(data.get("event", {}))
        except Exception as e:
            state.connected = False
            await asyncio.sleep(2)

async def main():
    asyncio.create_task(listen_to_ws())
    
    with Live(generate_ui(), refresh_per_second=4) as live:
        while True:
            await asyncio.sleep(0.25)
            live.update(generate_ui())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
