import os
import subprocess
import sys
import platform

def run_command(command, shell=True):
    print(f"\nRunning: {command}")
    subprocess.run(command, shell=shell, check=True)

def create_directory(path):
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

def main():
    # 1. Run setup.py install
    run_command("python setup.py install")

    # 2. Create export directory
    create_directory("data/export")

    # 3. Create virtual environment
    run_command("python3 -m venv venv")

    # 4. Install dependencies in virtual environment
    current_os = platform.system()

    print("Installing dependencies in virtual environment...")
    if current_os == "Windows":
        command = "venv\\Scripts\\activate && pip install -r requirements.txt"
        run_command(command)
    elif current_os in ["Darwin", "Linux"]:
        # bash workaround to run in a sub-shell to activate venv
        command = ". venv/bin/activate && pip install -r requirements.txt"
        run_command(command)
    else:
        print("Unsupported OS detected. Please install dependencies manually.")
        sys.exit(1)

    print("\nProject setup complete! You can now start working with the virtual environment.")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        sys.exit(1)