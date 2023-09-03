import subprocess

class PlotLibProgress:
    @staticmethod
    def _get_estimated_completion_datetime():
        pass

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
    def _get_gpu_data_from_host():
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
    def _get_commitment_atx():
        pass

    @staticmethod
    def _get_id():
        pass

    @staticmethod
    def _get_postcli_version():
        pass

    @staticmethod
    def _get_hostname():
        pass

    @staticmethod
    def _get_labels():
        pass

    @staticmethod
    def _get_num_units():
        pass

    @staticmethod
    def _get_max_file_size_gib():
        pass

    @staticmethod
    def _get_nonce():
        pass

    @staticmethod
    def _get_post_data_dir():
        pass

    @staticmethod
    def _get_post_data_size_gib():
        pass