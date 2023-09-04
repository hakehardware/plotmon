import json
from time import sleep
from rich.live import Live
from views import GraphicsMon, ProgressMon, InfoMon, IdMon, Header, GenLayout
import utils
    
def main():
    
    # Get Config
    config = utils.get_config()

    if config == None:
        exit

    # Initialize Classes
    graphics_mon = GraphicsMon()
    info_mon = InfoMon()
    id_mon = IdMon()
    progress_mon = ProgressMon(config)

    # Create Layout
    layout = GenLayout.layout()
    layout["gpu_info"].update(graphics_mon.create_panel())
    layout["plot_info"].update(info_mon.create_panel(config))
    layout["plot_progress"].update(progress_mon.create_panel())
    layout["plot_ids"].update(id_mon.create_panel(config))
    layout["header"].update(Header())

    # Print Layout
    with Live(layout, refresh_per_second=1, screen=True):
        while True:
            sleep(1)
            graphics_mon.update_panel()
            progress_mon.update_panel()

if __name__ == "__main__":
    main()
