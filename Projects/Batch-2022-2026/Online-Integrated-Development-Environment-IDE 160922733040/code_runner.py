"""
Safe Python code execution via subprocess.
Runs user code in an isolated subprocess with timeout.
"""
import subprocess
import sys
import tempfile
import os

BLOCKED_IMPORTS = {'os', 'subprocess', 'shutil', 'pathlib', 'sys', 'socket',
                   'http', 'urllib', 'requests', 'ftplib', 'smtplib',
                   'ctypes', 'multiprocessing', 'signal', 'pty'}

TIMEOUT_SECONDS = 10


def check_safety(code):
    """Check code for potentially dangerous operations."""
    warnings = []
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Check imports
        if stripped.startswith('import ') or stripped.startswith('from '):
            for blocked in BLOCKED_IMPORTS:
                if blocked in stripped:
                    warnings.append(f"Line {i}: Import '{blocked}' is blocked for security.")
        # Check dangerous functions
        if 'open(' in stripped and ('w' in stripped or 'a' in stripped):
            warnings.append(f"Line {i}: File write operations are not allowed.")
        if 'exec(' in stripped or 'eval(' in stripped:
            warnings.append(f"Line {i}: exec/eval calls are restricted.")
        if '__import__' in stripped:
            warnings.append(f"Line {i}: __import__ is not allowed.")
    return warnings


def run_python(code):
    """Execute Python code safely and return stdout, stderr, and status."""
    # Safety check
    warnings = check_safety(code)
    if warnings:
        return {
            'stdout': '',
            'stderr': 'Security Warning:\n' + '\n'.join(warnings),
            'status': 'blocked',
            'exit_code': -1
        }

    # Write code to temp file
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name

        # Run in subprocess
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=tempfile.gettempdir()
        )

        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'status': 'success' if result.returncode == 0 else 'error',
            'exit_code': result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Execution timed out after {TIMEOUT_SECONDS} seconds.',
            'status': 'timeout',
            'exit_code': -1
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'status': 'error',
            'exit_code': -1
        }
    finally:
        try:
            os.unlink(temp_path)
        except Exception:
            pass
