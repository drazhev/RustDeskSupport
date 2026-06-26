"""
RustDesk launcher за клиенти на drazhev.net
Записва конфига и стартира RustDesk с предварително зададени сървъри.
"""

import os
import sys
import shutil
import tempfile
import subprocess
import atexit


CONFIG_CONTENT = """\
[options]
custom-rendezvous-server = "192.168.222.21"
relay-server = "192.168.222.21"
api-server = "http://192.168.222.21:21114"
key = "PyMhoZr13G9aPMgshwW7XHzV86jU+MIssK80Nh9GYzc="
"""


def resource_path(filename):
    """Връща пътя до вграден файл (работи и при PyInstaller .exe)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, filename)


def write_config():
    """Записва конфига в стандартната RustDesk папка."""
    config_dir = os.path.join(os.environ["APPDATA"], "RustDesk", "config")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "RustDesk2.toml")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(CONFIG_CONTENT)


def main():
    # Записваме конфига преди стартиране
    write_config()

    # Копираме rustdesk.exe във временна папка и го стартираме
    work_dir = tempfile.mkdtemp(prefix="rustdesk_drazhev_")
    atexit.register(shutil.rmtree, work_dir, ignore_errors=True)

    src_exe = resource_path("rustdesk.exe")
    dst_exe = os.path.join(work_dir, "rustdesk.exe")
    shutil.copy2(src_exe, dst_exe)

    subprocess.run([dst_exe], cwd=work_dir)


if __name__ == "__main__":
    main()
