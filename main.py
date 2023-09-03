from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table


console = Console()


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )

    layout["side"].split(Layout(name="gpu_info"), Layout(name="plot_info"))
    layout["body"].split(Layout(name="plot_progress"), Layout(name="ids"))

    return layout

def make_gpu_info() -> Panel:

    message_panel = Panel(
        "GPU Data Goes here",
        box=box.ROUNDED,
        padding=(1, 2),
        title="GPU Info",
        border_style="bright_blue",
    )

    return message_panel

def make_plot_progress() -> Panel:

    message_panel = Panel(
        "Plot Progress Goes here",
        box=box.ROUNDED,
        padding=(1, 2),
        title="Plot Progress",
        border_style="bright_blue",
    )

    return message_panel

def make_ids() -> Panel:

    message_panel = Panel(
        "ID Info Goes Here",
        box=box.ROUNDED,
        padding=(1, 2),
        title="IDs",
        border_style="bright_blue",
    )

    return message_panel

def make_plot_info() -> Panel:

    message_panel = Panel(
        "Plot Info Goes Here",
        box=box.ROUNDED,
        padding=(1, 2),
        title="Plot Info",
        border_style="bright_blue",
    )

    return message_panel

def make_header() -> Panel:

    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="center", ratio=1)
    grid.add_column(justify="right")

    grid.add_row(
        "PlotMon",
        "Subscribe to my [link=https://www.youtube.com/channel/UCakvG7QQp4oL0Rtpiei1yKg]YouTube[/link] for more Spacemesh content!",
        datetime.now().ctime().replace(":", "[blink]:[/]"),
    )

    return Panel(grid)
    

layout = make_layout()

from time import sleep

from rich.live import Live

with Live(layout, refresh_per_second=10, screen=True):
    while True:
        sleep(0.1)
        layout["gpu_info"].update(make_gpu_info())
        layout["plot_info"].update(make_plot_info())
        layout["plot_progress"].update(make_plot_progress())
        layout["ids"].update(make_ids())
        layout["header"].update(make_header())
