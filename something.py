import os
import subprocess

def process_file_via_command(filename):
    """
    Processes a file by executing an external command.
    Vulnerability: Command Injection due to direct concatenation of user input.
    """
    if not isinstance(filename, str):
        print("Error: Filename must be a string.")
        return

    # Vulnerable line: Directly embedding user input into an OS command string.
    # A malicious user could add additional commands after the filename.
    command = f"cat {filename}"
    print(f"Attempting to execute: '{command}'")

    try:
        # Using subprocess.run is generally better than os.system for security,
        # but the vulnerability here lies in the 'command' string itself.
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print("Command output:")
        print(result.stdout)
        if result.stderr:
            print("Command error (stderr):")
            print(result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Error: Command '{command.split()[0]}' not found. Is 'cat' installed?")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def create_dummy_file(name, content):
    """Helper to create a dummy file for testing."""
    try:
        with open(name, "w") as f:
            f.write(content)
        print(f"Created dummy file: {name}")
    except IOError as e:
        print(f"Error creating file {name}: {e}")

def clean_up_dummy_file(name):
    """Helper to clean up a dummy file."""
    try:
        if os.path.exists(name):
            os.remove(name)
            print(f"Cleaned up dummy file: {name}")
    except OSError as e:
        print(f"Error cleaning up file {name}: {e}")

if __name__ == "__main__":
    dummy_file_name = "test_file.txt"
    create_dummy_file(dummy_file_name, "This is the content of the test file.")
    create_dummy_file("secret.txt", "TOP SECRET INFO!") # A file we want to protect

    print("\n--- Testing with safe input ---")
    process_file_via_command(dummy_file_name)

    print("\n--- Testing with malicious input (Command Injection attempt) ---")
    # This input will cause the command to become:
    # cat test_file.txt; ls -la;
    # which will list directory contents in addition to 'catting' the file.
    malicious_input = "test_file.txt; ls -la"
    process_file_via_command(malicious_input)

    print("\n--- More malicious input (attempt to read a sensitive file) ---")
    # This input could be used to read a file like 'secret.txt'
    malicious_input_2 = "test_file.txt; cat secret.txt"
    process_file_via_command(malicious_input_2)

    print("\n--- Cleanup ---")
    clean_up_dummy_file(dummy_file_name)
    clean_up_dummy_file("secret.txt")