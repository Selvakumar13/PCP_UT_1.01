import psutil

software_names = ['PCP_UT_1.01.exe', 'PCP_2.0.6.exe','PCP Utility.exe']

        # Iterate over all processes
for process in psutil.process_iter(['pid', 'name']):
            try:
                process_name = process.info['name'].lower()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Handle exceptions that might occur when accessing process information
                continue

            # Check if any of the specified software names is present in the process name
            if any(soft_instance.lower() in process_name for soft_instance in software_names):
                try:
                    # Terminate the process
                    print(process)
                    process.kill()
                    print(process)
                except psutil.NoSuchProcess:
                    pass  # Handle the case w



