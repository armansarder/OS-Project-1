import subprocess
import sys

MENU_TEXT = (
    "\Commands:\n"
    " password\n"
    " encrypt\n"
    " decrypt\n"
    " history\n"
    " quit\n"
)

def is_letters_only(text: str) -> bool:
    if text == "":
        return False
    for char in text:
        if not char.isalpha():
            return False
    return True 

def normalize_text(text: str) -> str:
    return text.strip().upper()
def send_to_logger(logger_process: subprocess.Popen, message: str) -> None:
    if logger_process.stdin is None:
        return

    logger_process.stdin.write(message + "\n")
    logger_process.stdin.flush()
    
import subprocess
import sys


MENU_TEXT = (
    "\nCommands:\n"
    "  password\n"
    "  encrypt\n"
    "  decrypt\n"
    "  history\n"
    "  quit\n"
)

def is_letters_only(text: str) -> bool:
    if text == "":
        return False

    for char in text:
        if not char.isalpha():
            return False

    return True


def normalize_text(text: str) -> str:
    return text.strip().upper()

def send_to_logger(logger_process: subprocess.Popen, message: str) -> None:
    if logger_process.stdin is None:
        return

    logger_process.stdin.write(message + "\n")
    logger_process.stdin.flush()

def send_to_encryptor(encryptor_process: subprocess.Popen, message: str) -> str:
    if encryptor_process.stdin is None or encryptor_process.stdout is None:
        return "ERROR Encryptor communication failure"

    encryptor_process.stdin.write(message + "\n")
    encryptor_process.stdin.flush()

    response = encryptor_process.stdout.readline()
    if response == "":
        return "ERROR Encryptor communication failure"

    return response.strip()


def show_history(history: list[str]) -> None:
    print("\nHistory:")

    if len(history) == 0:
        print("  (empty)")
        return

    for index in range(len(history)):
        print(f"  {index + 1}. {history[index]}")

def get_string_from_user(history: list[str], purpose: str) -> str | None:
    while True:
        print(f"\nChoose input for {purpose}:")
        print("  1. Enter a new string")
        print("  2. Choose from history")
        print("  3. Cancel")
        choice = input("Selection: ").strip()

        if choice == "1":
            user_text = input(f"Enter the string to {purpose}: ").strip()
            normalized = normalize_text(user_text)

            if not is_letters_only(normalized):
                print("Error: input must contain letters only.")
                continue

            return normalized

        if choice == "2":
            if len(history) == 0:
                print("History is empty.")
                continue

            show_history(history)
            selection = input("Enter history number or 0 to go back: ").strip()

            if selection == "0":
                continue

            if not selection.isdigit():
                print("Error: please enter a valid number.")
                continue

            index = int(selection) - 1
            if index < 0 or index >= len(history):
                print("Error: history selection out of range.")
                continue

            return history[index]

        if choice == "3":
            return None

        print("Error: invalid menu selection.")



def handle_password(encryptor_process: subprocess.Popen, logger_process: subprocess.Popen, history: list[str]) -> None:
    selected_text = get_string_from_user(history, "set as the passkey")

    if selected_text is None:
        print("Password update cancelled.")
        send_to_logger(logger_process, "COMMAND password cancelled")
        return

    send_to_logger(logger_process, "COMMAND password command received")
    response = send_to_encryptor(encryptor_process, f"PASSKEY {selected_text}")
    print(response)

    if response.startswith("RESULT"):
        send_to_logger(logger_process, "RESULT Password updated successfully")
    else:
        send_to_logger(logger_process, "ERROR Password update failed")

def handle_encrypt(encryptor_process: subprocess.Popen, logger_process: subprocess.Popen, history: list[str]) -> None:
    selected_text = get_string_from_user(history, "encrypt")

    if selected_text is None:
        print("Encryption cancelled.")
        send_to_logger(logger_process, "COMMAND encrypt cancelled")
        return
    if selected_text not in history:
        history.append(selected_text)
    send_to_logger(logger_process, "COMMAND encrypt command received")
    response = send_to_encryptor(encryptor_process, f"ENCRYPT {selected_text}")
    print(response)
    if response.startswith("RESULT "):
        result_text = response[7:]
        if result_text not in history:
            history.append(result_text)
        send_to_logger(logger_process, "RESULT Encryption succeeded")
    else:
        send_to_logger(logger_process, "ERROR Encryption failed")

def handle_decrypt(encryptor_process: subprocess.Popen, logger_process: subprocess.Popen, history: list[str]) -> None:
    selected_text = get_string_from_user(history, "decrypt")

    if selected_text is None:
        print("Decryption cancelled.")
        send_to_logger(logger_process, "COMMAND decrypt cancelled")
        return

    if selected_text not in history:
        history.append(selected_text)

    send_to_logger(logger_process, "COMMAND decrypt command received")
    response = send_to_encryptor(encryptor_process, f"DECRYPT {selected_text}")
    print(response)

    if response.startswith("RESULT "):
        result_text = response[7:]
        if result_text not in history:
            history.append(result_text)
        send_to_logger(logger_process, "RESULT Decryption succeeded")
    else:
        send_to_logger(logger_process, "ERROR Decryption failed")
def shutdown_processes(encryptor_process: subprocess.Popen, logger_process: subprocess.Popen) -> None:
    if encryptor_process.stdin is not None:
        encryptor_process.stdin.write("QUIT\n")
        encryptor_process.stdin.flush()
        encryptor_process.stdin.close()

    if logger_process.stdin is not None:
        logger_process.stdin.write("QUIT\n")
        logger_process.stdin.flush()
        logger_process.stdin.close()

    if encryptor_process.stdout is not None:
        encryptor_process.stdout.close()

    encryptor_process.wait()
    logger_process.wait()

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 driver.py <logfile>")
        return 1

    log_file = sys.argv[1]
    try:
        logger_process = subprocess.Popen(
            [sys.executable, "logger.py", log_file],
            stdin=subprocess.PIPE,
            text=True,
        )
        encryptor_process = subprocess.Popen(
            [sys.executable, "encryptor.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        print(f"Failed to start child processes: {exc}")
        return 1

    history: list[str] = []
    send_to_logger(logger_process, "START Driver started")
    try:
        while True:
            print(MENU_TEXT)
            command = input("Enter command: ").strip().lower()

            if command == "password":
                handle_password(encryptor_process, logger_process, history)
            elif command == "encrypt":
                handle_encrypt(encryptor_process, logger_process, history)
            elif command == "decrypt":
                handle_decrypt(encryptor_process, logger_process, history)
            elif command == "history":
                send_to_logger(logger_process, "COMMAND history command received")
                show_history(history)
                send_to_logger(logger_process, "RESULT History displayed")
            elif command == "quit":
                send_to_logger(logger_process, "EXIT Driver exiting")
                break
            else:
                print("Error: unknown command.")
                send_to_logger(logger_process, "ERROR Unknown driver command")
    finally:
        shutdown_processes(encryptor_process, logger_process)

    return 0
if __name__ == "__main__":
    raise SystemExit(main())