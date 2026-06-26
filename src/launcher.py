"""
RustDesk launcher за клиенти на drazhev.net
Записва конфига, логва се към акаунта на техника и стартира RustDesk.
"""

import os
import sys
import uuid
import json
import shutil
import tempfile
import subprocess
import atexit

try:
    import urllib.request as urlreq
except ImportError:
    urlreq = None

# --- Конфигурация (различна за всеки техник) ---
TECH_USERNAME = "drazhev"
TECH_PASSWORD = "drazhev123"
API_URL       = "http://hjc0a1kp4be.vpn.mynetname.net:21114"

SERVER_CONFIG = """\
[options]
custom-rendezvous-server = "hjc0a1kp4be.vpn.mynetname.net"
relay-server = "hjc0a1kp4be.vpn.mynetname.net"
api-server = "{api_url}"
key = "PyMhoZr13G9aPMgshwW7XHzV86jU+MIssK80Nh9GYzc="
""".format(api_url=API_URL)
# ------------------------------------------------


def resource_path(filename):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, filename)


def get_device_id():
    """Генерира уникален device ID за тази машина."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.getnode())))


def api_login():
    """Логва се към API-то и връща access_token или None."""
    try:
        payload = json.dumps({
            "username": TECH_USERNAME,
            "password": TECH_PASSWORD,
            "id": get_device_id(),
            "uuid": get_device_id(),
        }).encode()
        req = urlreq.Request(
            f"{API_URL}/api/login",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlreq.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("access_token")
    except Exception:
        return None


def write_config(token=None):
    """Записва RustDesk2.toml и ако има token — и ProfileCurrent.toml."""
    config_dir = os.path.join(os.environ["APPDATA"], "RustDesk", "config")
    os.makedirs(config_dir, exist_ok=True)

    with open(os.path.join(config_dir, "RustDesk2.toml"), "w", encoding="utf-8") as f:
        f.write(SERVER_CONFIG)

    if token:
        profile = f'access_token = "{token}"\n'
        with open(os.path.join(config_dir, "ProfileCurrent.toml"), "w", encoding="utf-8") as f:
            f.write(profile)


def main():
    token = api_login()
    write_config(token)

    work_dir = tempfile.mkdtemp(prefix="rustdesk_drazhev_")
    atexit.register(shutil.rmtree, work_dir, ignore_errors=True)

    src_exe = resource_path("rustdesk.exe")
    dst_exe = os.path.join(work_dir, "rustdesk.exe")
    shutil.copy2(src_exe, dst_exe)

    subprocess.run([dst_exe], cwd=work_dir)


if __name__ == "__main__":
    main()
