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

    # Detect the current operating system
    current_os = platform.system()

    if current_os == "Windows":
        print("Detected OS: Windows")

        # Create virtual environment
        print("Creating virtual environment...")
        run_command("python -m venv venv")

        # Install dependencies in virtual environment
        print("Installing dependencies in virtual environment...")
        run_command("venv\\Scripts\\activate && pip install -r requirements.txt")

        # Run setup.py install
        print("Running setup.py install...")
        run_command("python setup.py install")

    elif current_os in ["Darwin", "Linux"]:
        print("Detected OS: macOS/Linux")

        # Create virtual environment
        print("Creating virtual environment...")
        run_command("python3 -m venv venv")

        # Install dependencies in virtual environment
        print("Installing dependencies in virtual environment...")
        run_command(". venv/bin/activate && pip install -r requirements.txt")

        # Run setup.py install
        print("Running setup.py install...")
        run_command("python3 setup.py install")

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