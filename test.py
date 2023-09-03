import json
from plot_lib import PlotLibGpu

def main():
    config = None
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    if config == None:
        print('No Config')
        exit
    else:
        print(json.dumps(config))

    print(json.dumps(PlotLibGpu._get_gpu_data_from_host()))

main()