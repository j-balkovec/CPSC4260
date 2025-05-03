# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sat Apr 19th, 2025
#
# __file__: new_gui.py
#
# __brief__: TODO

# IDK HOW THIS WORKS with logging and message passing

import os
import json

from get_file_info import extract_file_info, save_to_json
from save_refactored import save_refactored_file
from analyze import code_metrics, halstead_metrics, find_code_smells
from exceptions import (FileReadError, CorruptFileError, FileNotFoundError,
                        FileEmptyError, FileTypeUnsupportedError, FileDecodeError,
                        FileLockedError, FileTooLargeError, FileOpenError)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    print("[*]\tWelcome to the Code Smell Detector (Terminal Edition)")
    print("--------------------------------------------------------")
    print("[*]\tUpload a file to get started")
    print("[*]\tAnalyze the file for code smells")
    print("[*]\tRefactor duplicate code")
    print("[*]\tSave the results")
    print("[*]\tExit the application")
    print("--------------------------------------------------------")

def upload_file():
    path = input("Enter path to code file: ").strip()
    if not os.path.isfile(path):
        print("[⛔️] File not found.")
        return None, None
    try:
        with open(path, "r") as f:
            metadata = extract_file_info(f)
            save_to_json(metadata)
            print(f"✅ File '{os.path.basename(path)}' uploaded successfully.")
            return path, metadata["Data"]
    except (FileReadError, CorruptFileError, FileNotFoundError, FileEmptyError,
            FileTypeUnsupportedError, FileDecodeError, FileLockedError,
            FileTooLargeError, FileOpenError) as e:
        print(f"[⛔️] Error opening file: {e.what()}")
    except Exception as e:
        print(f"[⛔️] Unexpected error: {e}")
    return None, None

def analyze_file(filepath):
    if not filepath:
        print("[⛔️] Please upload a file first.")
        return

    print("\n🔍 Analyzing file...")
    code_m = code_metrics(filepath)
    halstead_m = halstead_metrics(filepath)
    
    code_smells = find_code_smells(filepath)

    print("\n[*] Code Metrics:")
    for key, val in code_m.items():
        print(f"  - {key}: {val}")

    print("\n[*] Halstead Metrics:")
    for key, val in halstead_m.items():
        print(f"  - {key}: {val}")
        
    print("\n[*] Code Smells Found:") # Fix
    for smell in code_smells:
        for key, val in smell:
            print(f"  - {key}: {val}")

def refactor_code(filepath):
    if not filepath:
        print("[⛔️] Please upload a file first.")
        return

    print("🛠️ Refactoring duplicate code...")
    try:
        save_refactored_file(filepath)
        print("[✅] Refactoring complete.")
    except Exception as e:
        print(f"[⛔️] Error during refactoring: {e}")

def save_results():
    filename = input("Enter filename to save results (e.g., results.json): ").strip()
    if not filename:
        print("[⛔️] Invalid filename.")
        return
    try:
        # assuming metadata.json was previously saved
        with open("metadata.json", "r") as infile:
            data = json.load(infile)
        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=2)
        print(f"[✅] Results saved to {filename}")
    except Exception as e:
        print(f"[⛔️] Error saving results: {e}")

def main():
    filepath = None
    code_str = ""

    clear_terminal()
    print_welcome()

    while True:
        print("\nOptions:")
        print("-u Upload File")
        print("-a Analyze File")
        print("-rd Refactor Duplicates")
        print("-s Save Results")
        print("-c Clear Output")
        print("-q Exit")
        choice = input("Select a flag: ").strip()

        if choice == "-u":
            filepath, code_str = upload_file()
        elif choice == "-a":
            analyze_file(filepath)
        elif choice == "-rd":
            refactor_code(filepath)
        elif choice == "-s":
            save_results()
        elif choice == "-c":
            clear_terminal()
            print_welcome()
        elif choice == "-q":
            print("[*] Goodbye!")
            break
        else:
            print("[⛔️] Invalid option. Try again.")

if __name__ == "__main__":
    main()