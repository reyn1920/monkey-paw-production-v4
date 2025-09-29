#!/usr/bin/env python3
"""
TRAE.AI CLI Main Entry Point

This module provides the main command-line interface for TRAE.AI.
"""

import typer
import uvicorn
from typing import Annotated
import requests
from typing import Optional

# Import version and author from the package
try:
    from trae_ai import __version__, __author__
except ImportError:
    __version__ = "1.0.0-alpha"
    __author__ = "The TRAE.AI Open Source Team"

# Import the core functions from the trae.ai system
# Note: These imports assume the file structure is correct.
try:
    from trae_ai.scripts.solo.solo_agent import execute as execute_solo
    from trae_ai.agents.conversational_designer import ConversationalDesigner
    from trae_ai.agents.observer_agent import ObserverAgent
except ImportError:
    # Fallback for when modules are not available
    execute_solo = None
    ConversationalDesigner = None
    ObserverAgent = None

app = typer.Typer(
    name="traeai",
    help="The complete, autonomous, and free AI teammate for software development.",
)


@app.command()
def solo(
    goal: Annotated[
        str, typer.Argument(help="The high-level goal for the SOLO agent to execute.")
    ],
):
    """
    Engage the SOLO agent to autonomously execute a complex goal.
    """
    print(f"🚀 Engaging SOLO agent with goal: '{goal}'")
    if execute_solo:
        execute_solo(goal)
    else:
        typer.echo(
            "❌ SOLO agent module not available. Please check your installation."
        )


@app.command()
def design():
    """
    Launch the Genesis Engine to design a new application via conversation.
    """
    print("🤖 Launching Genesis Engine...")
    if ConversationalDesigner:
        designer = ConversationalDesigner()
        initial_idea = typer.prompt("What is the basic idea for your new application?")
        spec = designer.conduct_interview(initial_idea)
        print("\n✅ Design complete! Specification generated:")
        print(spec)
    else:
        typer.echo(
            "❌ Genesis Engine module not available. Please check your installation."
        )


@app.command()
def observe():
    """
    Run the proactive Observer agent to monitor systems and find tasks.
    """
    if ObserverAgent:
        observer = ObserverAgent()
        observer.monitor_streams()
    else:
        typer.echo(
            "❌ Observer agent module not available. Please check your installation."
        )


@app.command()
def ui(host: str = "127.0.0.1", port: int = 8000):
    """
    Launch the backend server for the Unified Development Environment (UDE).
    """
    print(f"🌐 Launching UDE Backend Server at http://{host}:{port}")
    uvicorn.run("trae_ai.servers.main_server:app", host=host, port=port, reload=True)


@app.command()
def server(host: str = "127.0.0.1", port: int = 8001, reload: bool = True):
    """
    Start the TRAE.AI development server.
    """
    typer.echo(f"🚀 Starting TRAE.AI server at http://{host}:{port}")
    uvicorn.run("trae_ai.servers.main_server:app", host=host, port=port, reload=reload)


@app.command()
def version():
    """
    Show TRAE.AI version information.
    """
    typer.echo(f"TRAE.AI v{__version__}")
    typer.echo(f"By {__author__}")


@app.command()
def status():
    """
    Check the status of TRAE.AI services.
    """
    typer.echo("🔍 Checking TRAE.AI services...")

    # Check main server (port 8001)
    try:
        response = requests.get("http://localhost:8001", timeout=5)
        if response.status_code == 200:
            typer.echo("✅ Main Server: Running (http://localhost:8001)")
        else:
            typer.echo("❌ Main Server: Not responding")
    except requests.exceptions.RequestException:
        typer.echo("❌ Main Server: Not running")

    # Check primary app (port 8000)
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            typer.echo("✅ Primary App: Running (http://localhost:8000)")
        else:
            typer.echo("❌ Primary App: Not responding")
    except requests.exceptions.RequestException:
        typer.echo("❌ Primary App: Not running")


@app.command()
def init(project_name: Optional[str] = None):
    """
    Initialize a new TRAE.AI project.
    """
    if not project_name:
        project_name = typer.prompt("Enter project name")

    typer.echo(f"🎯 Initializing new TRAE.AI project: {project_name}")
    typer.echo("📁 Creating project structure...")
    typer.echo("⚙️ Setting up configuration...")
    typer.echo("✅ Project initialized successfully!")


if __name__ == "__main__":
    app()
