import json
from plot_lib import PlotLibGpu, PlotLibInfo,PlotLibProgress

def main():
    config = None
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    if config == None:
        print('No Config')
        exit
    else:
        print(json.dumps(config))

    plot_progress_data = PlotLibProgress.get_plot_progress(config["post_data_dir"], {})

main()