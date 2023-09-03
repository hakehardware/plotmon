from datetime import datetime
import json
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from time import sleep
import time
from rich.live import Live
from plot_lib import PlotLibGpu, PlotLibInfo, PlotLibProgress
from rich import print
from rich.status import Status


VERSION = "v0.0.1"

console = Console()

class GPUInfo:
    def create_panel(self) -> Panel:
        self.gpu_status = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[green]{task.fields[gpu_value]}")
        )
        gpu_info = PlotLibGpu.get_gpu_data_from_host()[0]

        self.task_ids = {
            "GPU Temp": self.gpu_status.add_task("[green]Temperature", gpu_value=f'{gpu_info["Temp GPU"]}\u00b0C', total=100),
            "GPU Power": self.gpu_status.add_task("[green]Power", gpu_value=f'{gpu_info["Power Draw"]}W', total=800),
            "GPU Use": self.gpu_status.add_task("[green]GPU Use", gpu_value=f'{gpu_info["GPU Utilization"]}%', total=101),
            "GPU Mem Use": self.gpu_status.add_task("[green]Mem Use", gpu_value=f'{gpu_info["Memory Utilization"]}%', total=101),
            "GPU Fan Speed": self.gpu_status.add_task("[green]Fan Speed", gpu_value=f'{gpu_info["Fan Speed"]}%', total=101)
        }

        gpu_table = Table.grid(expand=True)

        gpu_table.add_row(
            Panel(
                self.gpu_status,
                title=gpu_info["Name"],
                border_style="green",
                padding=(1, 1),
            )
        )

        return gpu_table
    
    def update_gpu_task(self, task_name, completed, gpu_value):
        task_id = self.task_ids[task_name]
        self.gpu_status.update(task_id, completed=completed, gpu_value=gpu_value)

class PlotProgress:
    def __init__(self, config):
        self.config = config
        self.initial_total_file_size = None
        self.first_heartbeat_time = time.time()
        self.beats = 0

    def create_panel(self) -> Panel:

        self.plot_status = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%")
        )

        plot_progress_data = PlotLibProgress.get_plot_progress(self.config["post_data_dir"])

        self.task_ids = {
            "Total Progress": self.plot_status.add_task("[green]Total Progress", completed=plot_progress_data["Total Progress"], total=100),
            "File Progress": self.plot_status.add_task(f'[green]{plot_progress_data["Current File"]["File Name"]}', completed=plot_progress_data["File Progress"], total=100),
        }

        plot_progress_table = Table.grid(expand=True)
        plot_progress_table.add_column()
        plot_progress_table.add_column()

        self.initial_total_file_size = plot_progress_data["Current Total File Size"]
        self.beats += 1

        estimation_table = Table.grid()
        estimation_table.add_column(min_width=30)
        estimation_table.add_column()

        self.time_remaining = Status("Waiting for more beats")
        self.completion_date = Status("Waiting for more beats")
        self.speed = Status("Waiting for more beats")
        self.beats_str = Status(str(self.beats))

        estimation_table.add_row("Completion Date:", self.completion_date)
        estimation_table.add_row("Time Remaining:", self.time_remaining)
        estimation_table.add_row("Speed:", self.speed)
        estimation_table.add_row("Beats:", self.beats_str)

        plot_progress_table.add_row(
            Panel(
                self.plot_status,
                title="Plot Progress",
                border_style="green",
                padding=(1, 1),
            ),
            Panel(
                estimation_table,
                box=box.ROUNDED,
                title="Estimations",
                padding=(1, 2),
            )
        )

        return plot_progress_table
    
    def update_panel(self):
        plot_progress_data = PlotLibProgress.get_plot_progress(self.config["post_data_dir"])

        self.plot_status.update(self.task_ids["Total Progress"], completed=plot_progress_data["Total Progress"])
        self.plot_status.update(self.task_ids["File Progress"], description=f'[green]{plot_progress_data["Current File"]["File Name"]}', completed=plot_progress_data["File Progress"])
        self.beats += 1
        self.beats_str.update(str(self.beats))

        if(self.beats > 10):
            plot_estimates = PlotLibProgress.get_plot_estimates(self.config["post_data_dir"], self.first_heartbeat_time, self.initial_total_file_size, plot_progress_data["Current Total File Size"])
            self.speed.update(plot_estimates["Speed"])
            self.completion_date.update(plot_estimates["Completion Date"])
            self.time_remaining.update(plot_estimates["Time Remaining"])

class PlotInfo:
    def create_panel(self, config) -> Panel:
        plot_info = PlotLibInfo.get_plot_info(config["post_data_dir"])

        plot_table = Table.grid()
        plot_table.add_column(min_width=20)
        plot_table.add_column(min_width=20)

       

        plot_table.add_row(
            "[b]Total Size:", f'{plot_info["Total Size GiB"]} GiB'
        )

        plot_table.add_row(
            "[b]Space Units (SU):", f'{plot_info["NumUnits"]}'
        )

        plot_table.add_row(
            "[b]Max File Size:", f'{plot_info["Max File Size GiB"]} GiB'
        )

        plot_table.add_row(
            "[b]Labels Per Unit:", f'{plot_info["Labels Per Unit"]}'
        )

        plot_table.add_row(
            "[b]Nonce Found:", f'{plot_info["Found Nonce"]}'
        )

        plot_table.add_row(
            "[b]Directory:", f'{config["post_data_dir"]}'
        )
        

        plot_panel = Panel(
            plot_table,
            box=box.ROUNDED,
            padding=(1, 2),
            title="Plot Info",
            border_style="bright_blue",
        )

        return plot_panel

    def update_panel(self):
        pass

class PlotIds:
    def create_panel(self, config) -> Panel:
        plot_info = PlotLibInfo.get_plot_info(config["post_data_dir"])

        plot_table = Table.grid()
        plot_table.add_column(min_width=25)
        plot_table.add_column()

        plot_table.add_row(
            "[b]Base64 Node ID:", f'{plot_info["Base64 Node ID"]}'
        )

        plot_table.add_row(
            "[b]Hex Node ID:", f'{plot_info["Hex Node ID"]}'
        )

        plot_table.add_row(
            "[b]Base64 ATX ID:", f'{plot_info["Base64 Commitment ATX ID"]}'
        )

        plot_table.add_row(
            "[b]Hex ATX ID:", f'{plot_info["Hex Commitment ATX ID"]}'
        )

        plot_panel = Panel(
            plot_table,
            box=box.ROUNDED,
            padding=(1, 2),
            title="Plot IDs",
            border_style="bright_blue",
        )

        return plot_panel

def make_layout() -> Layout:
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
    layout["body"].split(Layout(name="plot_progress"), Layout(name="plot_ids"))

    return layout

class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")

        grid.add_row(
            f"PlotMon {VERSION}",
            "https://www.youtube.com/channel/UCakvG7QQp4oL0Rtpiei1yKg for more Spacemesh content!",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )

        return Panel(grid)
    
def main():
    # Get Config
    config = None
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    if config == None:
        print('No Config')
        exit

    # Initialize Classes
    gpu = GPUInfo()
    plot_info = PlotInfo()
    plot_ids = PlotIds()
    plot_progress = PlotProgress(config)

    # Create Layout
    layout = make_layout()
    layout["gpu_info"].update(gpu.create_panel())
    layout["plot_info"].update(plot_info.create_panel(config))
    layout["plot_progress"].update(plot_progress.create_panel())
    layout["plot_ids"].update(plot_ids.create_panel(config))
    layout["header"].update(Header())

    # Print Layout
    with Live(layout, refresh_per_second=1, screen=True):
        while True:
            sleep(1)
            gpu_info = PlotLibGpu.get_gpu_data_from_host()[0]
            gpu.update_gpu_task("GPU Temp", completed=gpu_info["Temp GPU"], gpu_value=f'{gpu_info["Temp GPU"]}\u00b0C')
            gpu.update_gpu_task("GPU Power", completed=gpu_info["Power Draw"], gpu_value=f'{gpu_info["Power Draw"]}W')
            gpu.update_gpu_task("GPU Use", completed=gpu_info["GPU Utilization"], gpu_value=f'{gpu_info["GPU Utilization"]}%')
            gpu.update_gpu_task("GPU Mem Use", completed=gpu_info["Memory Utilization"], gpu_value=f'{gpu_info["Memory Utilization"]}%')
            gpu.update_gpu_task("GPU Fan Speed", completed=gpu_info["Fan Speed"], gpu_value=f'{gpu_info["Fan Speed"]}%')

            plot_progress.update_panel()

if __name__ == "__main__":
    main()
