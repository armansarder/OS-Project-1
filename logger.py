import sys
from datetime import datetime

def format_timestamp() -> str:
    """Returns the current timestamp formatted as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_log_message(line: str) -> tuple[str, str]:
    stripped = line.strip()

    if not stripped:
        return "INFO", ""

    parts = stripped.split(maxsplit=1)
    action = parts[0]
    message = parts[1] if len(parts) > 1 else ""
    return action, message

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python logger.py <log_file>", file=sys.stderr)
        return 1
    
    log_file = sys.argv[1]
    try: 
        with open(log_file, "a", encoding="utf-8") as logfile:
            for raw_line in sys.stdin:
                line = raw_line.rstrip("\n")
                
                if line == "QUIT":
                    break

                action, message = parse_log_message(line)
                timestamp = format_timestamp()
                logfile.write(f"{timestamp} [{action}] {message}\n")
                logfile.flush()
    except OSError as exc:
        print(f"Error opening log file: {exc}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())