import win32print
import time
import os
import json

def create_or_load_json(log_file_path):
    if not os.path.exists(log_file_path):
        # If the JSON file doesn't exist, create it with an empty dictionary
        with open(log_file_path, 'w') as json_file:
            json.dump({}, json_file)

def update_printed_pages(printer_name, log_file_path):
    try:
        # Read the current data from the JSON file
        with open(log_file_path, 'r') as json_file:
            printer_data = json.load(json_file)

        num_of_pages_printed = printer_data.get(printer_name, 0) + 1  # Increment the page count

        # Update the data in the JSON dictionary
        printer_data[printer_name] = num_of_pages_printed

        # Write the updated data back to the JSON file
        with open(log_file_path, 'w') as json_file:
            json.dump(printer_data, json_file, indent=4)

        print(f"Total pages printed for {printer_name}: {num_of_pages_printed}")

    except Exception as e:
        print(f"Error: {e}")

def count_printed_pages(log_file_path):
    try:
        initial_printer_name = None
        initial_pages_printed = 0

        while True:
            printer_name = win32print.GetDefaultPrinter()

            if printer_name != initial_printer_name:
                # A new printer is being used, update the initial values
                initial_printer_name = printer_name
                initial_pages_printed = 0

            hprinter = win32print.OpenPrinter(printer_name)
            printer_info = win32print.GetPrinter(hprinter, 2)
            final_pages_printed = printer_info['cJobs']
            win32print.ClosePrinter(hprinter)

            if final_pages_printed > initial_pages_printed:
                update_printed_pages(printer_name, log_file_path)
                initial_pages_printed = final_pages_printed

            # Sleep for a short interval before checking again (e.g., 1 second)
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the path to the JSON file where document counts will be stored
    log_file_path = "document_count.json"

    create_or_load_json(log_file_path)  # Create the JSON file if it doesn't exist
    count_printed_pages(log_file_path)
