from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table

from plot_lib import PlotLibGpu


console = Console()

class GPUInfo:
    def create_panel(self) -> Panel:
        self.gpu_status = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[green]{task.fields[gpu_value]}")
        )
        gpu_info = PlotLibGpu._get_gpu_data_from_host()[0]

        self.task_ids = {
            "GPU Temp": self.gpu_status.add_task("[green]Temperature", gpu_value=f'{gpu_info["Temp GPU"]}\u00b0C', total=100),
            "GPU Power": self.gpu_status.add_task("[green]Power", gpu_value=f'{gpu_info["Power Draw"]}W', total=800),
            "GPU Use": self.gpu_status.add_task("[green]GPU Use", gpu_value=f'{gpu_info["GPU Utilization"]}%', total=101),
            "GPU Mem Use": self.gpu_status.add_task("[green]Mem Use", gpu_value=f'{gpu_info["Memory Utilization"]}%', total=101),
            "GPU Fan Speed": self.gpu_status.add_task("[green]Fan Speed", gpu_value=f'{gpu_info["Fan Speed"]}%', total=101)
        }

        gpu_panel = Panel(
            self.gpu_status,
            title=gpu_info["Name"],
            border_style="green",
            padding=(1, 1),
        )

        return gpu_panel
    
    def update_gpu_task(self, task_name, completed, gpu_value):
        task_id = self.task_ids[task_name]
        self.gpu_status.update(task_id, completed=completed, gpu_value=gpu_value)

class PlotProgress:
    def create_panel(self) -> Panel:
        pass

    def update_panel(self):
        pass


class PlotInfo:
    def create_panel(self) -> Panel:
        pass

    def update_panel(self):
        pass


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
    layout["body"].split(Layout(name="plot_progress"), Layout(name="ids"))

    return layout

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







def main():
    gpu = GPUInfo()

    # ============= Layout
    layout = make_layout()
    layout["gpu_info"].update(gpu.create_panel())
    # layout["plot_info"].update(make_plot_info())
    # layout["plot_progress"].update(make_plot_progress())
    # layout["ids"].update(make_ids())
    layout["header"].update(make_header())

    with Live(layout, refresh_per_second=10, screen=True):
        while True:
            sleep(0.1)
            gpu_info = PlotLibGpu._get_gpu_data_from_host()[0]
            gpu.update_gpu_task("GPU Temp", completed=gpu_info["Temp GPU"], gpu_value=f'{gpu_info["Temp GPU"]}\u00b0C')
            gpu.update_gpu_task("GPU Power", completed=gpu_info["Power Draw"], gpu_value=f'{gpu_info["Power Draw"]}W')
            gpu.update_gpu_task("GPU Use", completed=gpu_info["GPU Utilization"], gpu_value=f'{gpu_info["GPU Utilization"]}%')
            gpu.update_gpu_task("GPU Mem Use", completed=gpu_info["Memory Utilization"], gpu_value=f'{gpu_info["Memory Utilization"]}%')
            gpu.update_gpu_task("GPU Fan Speed", completed=gpu_info["Fan Speed"], gpu_value=f'{gpu_info["Fan Speed"]}%')

if __name__ == "__main__":
    main()
