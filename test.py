import json
from plot_lib import PlotLibGpu, PlotLibInfo

def main():
    config = None
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    if config == None:
        print('No Config')
        exit
    else:
        print(json.dumps(config))

    plot_info = PlotLibInfo.get_plot_info(config["post_data_dir"])
    print(plot_info)

main()