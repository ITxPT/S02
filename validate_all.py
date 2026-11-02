"""
Runs every validation script (validate_json.py / test.py) in the S02 subfolders
and prints a summary. Exits with code 1 if anything failed.

Usage: python validate_all.py [-v]
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPT_NAMES = ["validate_json.py", "test.py"]

# Output markers used by the existing scripts
VALID_PATTERNS = [
    re.compile(r" - VALID$"),                                 # P04-P07
    re.compile(r" - Payload is valid according to schema\.$"),  # P01, P03
    re.compile(r"^Valid JSON$"),                              # P08
]
INVALID_PATTERNS = [
    re.compile(r" - INVALID!+$"),                             # P04-P07
    re.compile(r"^Invalid JSON!+$"),                          # P08
]
# P01/P03 only print this on failure (P04-P07 print it before an INVALID line)
VALIDATION_FAILED = re.compile(r"^Payload validation failed")
ERROR_PATTERNS = [
    re.compile(r"^Traceback \(most recent call last\)"),
    re.compile(r"^Error parsing XSD"),
]


def find_script(folder):
    for name in SCRIPT_NAMES:
        if os.path.isfile(os.path.join(folder, name)):
            return name
    return None


def run_script(folder, script):
    proc = subprocess.run(
        [sys.executable, script],
        cwd=folder,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def analyse_output(output):
    lines = output.splitlines()
    valid = sum(1 for l in lines if any(p.search(l) for p in VALID_PATTERNS))
    invalid = sum(1 for l in lines if any(p.search(l) for p in INVALID_PATTERNS))
    if invalid == 0:
        invalid = sum(1 for l in lines if VALIDATION_FAILED.search(l))
    errors = sum(1 for l in lines if any(p.search(l) for p in ERROR_PATTERNS))
    return valid, invalid, errors


def main():
    parser = argparse.ArgumentParser(description="Run all S02 validation scripts")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="always show the full output of each script")
    args = parser.parse_args()

    folders = sorted(
        d for d in os.listdir(ROOT)
        if os.path.isdir(os.path.join(ROOT, d)) and not d.startswith(".")
    )

    results = []
    for name in folders:
        folder = os.path.join(ROOT, name)
        script = find_script(folder)
        if script is None:
            results.append((name, None, 0, 0, "SKIPPED (no script)"))
            continue

        returncode, output = run_script(folder, script)
        valid, invalid, errors = analyse_output(output)

        if returncode != 0 or errors:
            status = f"ERROR (exit code {returncode})" if returncode != 0 else "ERROR"
        elif invalid:
            status = "FAIL"
        elif valid == 0:
            status = "ERROR (no results found)"
        else:
            status = "OK"

        if args.verbose or status != "OK":
            print(f"===== {name}/{script} =====")
            print(output.rstrip() or "(no output)")
            print()

        results.append((name, script, valid, invalid, status))

    width = max(len(r[0]) for r in results)
    print("===== SUMMARY =====")
    for name, script, valid, invalid, status in results:
        if script is None:
            print(f"{name:<{width}}  {'':<16}  {'':<10}  {status}")
        else:
            print(f"{name:<{width}}  {script:<16}  {valid:>3} valid  {invalid:>3} invalid  {status}")

    passed = sum(1 for r in results if r[4] == "OK")
    skipped = sum(1 for r in results if r[1] is None)
    failed = len(results) - passed - skipped
    print()
    print(f"TOTAL: {passed} passed, {failed} failed, {skipped} skipped")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
