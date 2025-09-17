import subprocess
import sys

subprocess.Popen([
    sys.executable, "-m", "streamlit", "run", "main.py"
])
