import os
import sys
import time
import urllib.request
import subprocess

def wait_for_service(url="http://127.0.0.1:3000/health", timeout=60):
    start = time.time()
    print(f"Waiting for {url} to become ready...")
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    print("Service is ready!")
                    return True
        except Exception:
            time.sleep(1)
    print("Timed out waiting for service.")
    return False

def take_screenshot(url, output_path, window_size="1400,1100"):
    cmd = [
        "/etc/profiles/per-user/zerok/bin/chromium",
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={window_size}",
        f"--screenshot={output_path}",
        url
    ]
    print(f"Capturing {url} -> {output_path}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(output_path):
        print(f"Successfully captured: {output_path} ({os.path.getsize(output_path)} bytes)")
        return True
    else:
        print(f"Failed to capture. Stderr: {res.stderr}")
        return False

def main():
    if not wait_for_service():
        sys.exit(1)
    
    os.makedirs("/home/zerok/projects/upward/screenshots", exist_ok=True)
    
    # 1. Capture Swagger Main Overview
    take_screenshot(
        "http://127.0.0.1:3000/docs/#/",
        "/home/zerok/projects/upward/screenshots/swagger_overview.png",
        window_size="1400,1200"
    )
    
    # 2. Capture Health endpoint
    take_screenshot(
        "http://127.0.0.1:3000/health",
        "/home/zerok/projects/upward/screenshots/health_endpoint.png",
        window_size="800,400"
    )

if __name__ == "__main__":
    main()
