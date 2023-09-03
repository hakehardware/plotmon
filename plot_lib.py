import subprocess
import json
from base64 import b64decode
import socket
import os
import re

class PlotLibProgress:
    @staticmethod
    def get_plot_progress(post_data_dir, plot_progress_data):
        post_progress_new = PlotLibProgress._get_file_progress(post_data_dir)
        print(post_progress_new)

        return {
            "Total Progress": post_progress_new["Total Progress"],
            "File Progress": post_progress_new["File Progress"],
            "Current File": post_progress_new["Current File"]
        }

    @staticmethod
    def _get_file_progress(post_data_dir):
        plotLibInfo = PlotLibInfo()
        plot_info = plotLibInfo.get_plot_info(post_data_dir)

        total_file_size_mib = plot_info["Total Size GiB"]*1024
        max_file_size_mib = plot_info["Max File Size GiB"]*1024

        post_data_size = 0
        file_metadata = []

        # Iterate through the files in the directory
        for filename in os.listdir(post_data_dir):
            if filename.startswith('postdata_') and filename.endswith('.bin'):
                file_path = os.path.join(post_data_dir, filename)
                match = re.search(r'_(\d+)\.', filename)

                # Get the file size
                size = os.path.getsize(file_path)
                post_data_size += size
                file_metadata.append({
                    'File Name': filename,
                    'Size MiB': str(size / (1024 * 1024)),
                    'Index': int(match.group(1))
                })
        print(float(file_metadata[-1]["Size MiB"]))
        print(max_file_size_mib)
        current_file = max(file_metadata, key=lambda x: x["Index"])
        total_progress = round((post_data_size / (1024*1024)) / total_file_size_mib, 2)*100
        file_progress = round(float(file_metadata[-1]["Size MiB"]) / max_file_size_mib, 2)*100

        return {
            "Total Progress": total_progress,
            "File Progress": file_progress,
            "Current File": current_file
        }
    
    @staticmethod
    def _get_elapsed_time_from_start_hour_min():
        pass

    @staticmethod
    def _get_current_postdata_file_progress_percent():
        pass

    @staticmethod
    def _get_current_postdata_file_name():
        pass

    @staticmethod
    def _get_elapsed_time_on_current_postdata_file_hour_min():
        pass

    @staticmethod
    def _get_completion_datetime():
        pass

    @staticmethod
    def _get_heartbeat_datetime():
        pass


class PlotLibGpu:
    @staticmethod
    def get_gpu_data_from_host():
        # Run nvidia-smi to get GPU information
        nvidia_smi_output = subprocess.check_output(
            [
                'nvidia-smi', 
                '--query-gpu=utilization.gpu,utilization.memory,temperature.gpu,fan.speed,power.draw,pstate,name', 
                '--format=csv,noheader,nounits'
            ], universal_newlines=True
        )

        # Split the output by lines
        gpu_data_lines = nvidia_smi_output.strip().split('\n')

        # Process the GPU information
        gpu_data = []

        for line in gpu_data_lines:
            gpu_utilization, memory_utilization, temp_gpu, fan_speed, power_draw, performance_state, name = line.strip().split(', ')

            if "N/A" in gpu_utilization:
                gpu_utilization = 0
            else:
                gpu_utilization = int(gpu_utilization)

            if "N/A" in memory_utilization:
                memory_utilization = 0
            else:
                memory_utilization = int(memory_utilization)

            if "N/A" in temp_gpu:
                temp_gpu = 0
            else:
                temp_gpu = int(temp_gpu)

            if "N/A" in fan_speed:
                fan_speed = 0
            else:
                fan_speed = int(fan_speed)

            if "N/A" in power_draw:
                power_draw = 0
            else:
                power_draw = float(power_draw)

            
            gpu_data.append({
                "GPU Utilization": gpu_utilization,
                "Memory Utilization": memory_utilization,
                "Temp GPU": temp_gpu,
                "Fan Speed": fan_speed,
                "Power Draw": power_draw,
                "Performance State": performance_state,
                "Name": name
        })

        return gpu_data


class PlotLibInfo:

    @staticmethod
    def get_plot_info(post_data_dir):

        nonce = None
        nonce_value = None
        found_nonce = False

        with open(post_data_dir + '/postdata_metadata.json') as f:
            metadata = f.read()

        parsed_metadata = json.loads(metadata)

        base64_node_id = parsed_metadata['NodeId']
        hex_node_id = b64decode(base64_node_id).hex()

        base64_commitment_atx_id = parsed_metadata['CommitmentAtxId']
        hex_commitment_atx_id = b64decode(base64_commitment_atx_id).hex()

        num_units = parsed_metadata['NumUnits']

        total_size_gib = num_units * 64

        max_file_size_gib = parsed_metadata['MaxFileSize'] / (1024*1024*1024)

        labels_per_unit = parsed_metadata['LabelsPerUnit']

        hostname = socket.gethostname()

        try:
            nonce = parsed_metadata['Nonce']
        except:
            pass

        try:
            nonce_value = parsed_metadata['NonceValue']
        except:
            pass

        if nonce_value and nonce:
            found_nonce = True

        return {
            "Base64 Node ID": base64_node_id,
            "Hex Node ID": hex_node_id,
            "Base64 Commitment ATX ID": base64_commitment_atx_id,
            "Hex Commitment ATX ID": hex_commitment_atx_id,
            "NumUnits": num_units,
            "Max File Size GiB": max_file_size_gib,
            "Labels Per Unit": labels_per_unit,
            "Nonce": nonce,
            "Nonce Value": nonce_value,
            "Hostname": hostname,
            "Total Size GiB": total_size_gib,
            "Found Nonce": found_nonce
        }