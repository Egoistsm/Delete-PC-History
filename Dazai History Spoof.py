import os
import sqlite3
import shutil
import subprocess
import psutil
from browser_history.browsers import Chrome, Firefox, Opera, Edge

def clear_temp_files():
    # ลบไฟล์ใน Temporary directories
    temp_dirs = [os.environ["TEMP"], os.environ["TMP"], os.path.expanduser("~/AppData/Local/Temp")]
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir):
                try:
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        shutil.rmtree(dir_path, ignore_errors=True)
                except Exception as e:
                    print(f"Error cleaning temp files: {e}")

def clear_browser_history():
    # ลบบันทึกประวัติในเบราว์เซอร์ (Chrome, Edge, Firefox, Opera)
    browsers = [Chrome, Firefox, Opera, Edge]
    for browser in browsers:
        try:
            b = browser()
            b.history().clear()  # ใช้งาน browser-history library
            print(f"Cleared history for {b.name}")
        except Exception as e:
            print(f"Failed to clear history for {b}: {e}")

def clear_browser_downloads():
    # เส้นทางที่เก็บประวัติการดาวน์โหลดของแต่ละเบราว์เซอร์
    history_files = {
        "Chrome": os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History"),
        "Edge": os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\History"),
        "Firefox": os.path.expanduser(r"~\AppData\Roaming\Mozilla\Firefox\Profiles"),
        "Opera GX": os.path.expanduser(r"~\AppData\Roaming\Opera Software\Opera GX Stable\History"),
    }

    for browser, path in history_files.items():
        try:
            if "Firefox" in browser:
                # จัดการกับ Firefox
                if os.path.exists(path):
                    for profile in os.listdir(path):
                        profile_path = os.path.join(path, profile)
                        if os.path.isdir(profile_path):
                            places_db = os.path.join(profile_path, "places.sqlite")
                            if os.path.exists(places_db):
                                try:
                                    conn = sqlite3.connect(places_db)
                                    cursor = conn.cursor()
                                    cursor.execute("DELETE FROM moz_downloads")  # ลบข้อมูลในตาราง moz_downloads
                                    conn.commit()
                                    conn.close()
                                    print(f"Cleared downloads for Firefox profile: {profile}")
                                except sqlite3.Error as e:
                                    print(f"Error clearing downloads for Firefox: {e}")
            else:
                # จัดการกับ Chrome, Edge, Opera GX
                if os.path.exists(path):
                    try:
                        conn = sqlite3.connect(path)
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM downloads")  # ลบข้อมูลในตาราง downloads
                        conn.commit()
                        conn.close()
                        print(f"Cleared downloads for {browser}.")
                    except sqlite3.Error as e:
                        print(f"Error clearing downloads for {browser}: {e}")
        except Exception as e:
            print(f"Error processing {browser}: {e}")

def uninstall_unused_programs():
    # ลบโปรแกรมที่ไม่ต้องการโดยตรวจสอบจาก Psutil
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if "some_unwanted_program" in proc.info['name'].lower():
                subprocess.call(["taskkill", "/F", "/PID", str(proc.info['pid'])])
    except Exception as e:
        print(f"Error uninstalling programs: {e}")

def clear_system_logs():
    # ลบ System Logs เช่น Event Viewer Logs
    try:
        subprocess.call(["wevtutil", "cl", "Application"], shell=True)
        subprocess.call(["wevtutil", "cl", "System"], shell=True)
        subprocess.call(["wevtutil", "cl", "Security"], shell=True)
        subprocess.call(["wevtutil", "cl", "Setup"], shell=True)
        print("Cleared system logs.")
    except Exception as e:
        print(f"Error clearing system logs: {e}")

def disable_prefetch_superfetch():
    # ลบ Prefetch & ปิดใช้งาน Superfetch
    prefetch_dir = "C:\\Windows\\Prefetch"
    if os.path.exists(prefetch_dir):
        try:
            shutil.rmtree(prefetch_dir)
            print("Prefetch cleared.")
        except Exception as e:
            print(f"Error clearing prefetch: {e}")
    
    # ปิด Superfetch (Windows)
    try:
        subprocess.call(["sc", "stop", "SysMain"])
        subprocess.call(["sc", "config", "SysMain", "start=", "disabled"])
        print("Disabled Superfetch.")
    except Exception as e:
        print(f"Error disabling Superfetch: {e}")

def clear_registry_keys():
    # ลบข้อมูลใน Windows Registry (เช่น Software Install Logs)
    try:
        reg_keys = [
            r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU",
            r"HKCU\Software\Microsoft\Internet Explorer\TypedURLs"
        ]
        for key in reg_keys:
            subprocess.call(["reg", "delete", key, "/f"], shell=True)
        print("Cleared registry keys.")
    except Exception as e:
        print(f"Error clearing registry keys: {e}")

def clear_recent_files():
    # โฟลเดอร์ที่เก็บ Recent Files
    recent_dir = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Recent')
    if os.path.exists(recent_dir):
        try:
            for recent_file in os.listdir(recent_dir):
                file_path = os.path.join(recent_dir, recent_file)
                if os.path.isfile(file_path) or os.path.islink(file_path):  # ตรวจสอบว่าเป็นไฟล์
                    os.unlink(file_path)  # ลบไฟล์หรือ symlink
            print("Cleared recent files.")
        except Exception as e:
            print(f"Error clearing recent files: {e}")

def clear_clipboard():
    try:
        import subprocess
        subprocess.run("echo off | clip", shell=True, check=True)  # ทำให้ Clipboard ว่างเปล่า
        print("Cleared clipboard.")
    except Exception as e:
        print(f"Error clearing clipboard: {e}")

"""def clear_browser_saved_passwords():
    # พื้นที่เก็บข้อมูลรหัสผ่านใน Chrome, Edge, Firefox, และ Opera GX
    user_data_dirs = [
        # สำหรับ Chrome
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"),
        # สำหรับ Microsoft Edge
        os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data"),
        # สำหรับ Firefox
        os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"),
        # สำหรับ Opera GX
        os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera GX Stable")
    ]

    for path in user_data_dirs:
        if "Firefox" in path:
            try:
                # Firefox: ลบไฟล์ logins.json และ key4.db ในแต่ละโปรไฟล์
                if os.path.exists(path):
                    for profile in os.listdir(path):
                        profile_path = os.path.join(path, profile)
                        if os.path.isdir(profile_path):
                            logins_path = os.path.join(profile_path, "logins.json")
                            key4_path = os.path.join(profile_path, "key4.db")
                            if os.path.exists(logins_path):
                                os.remove(logins_path)
                            if os.path.exists(key4_path):
                                os.remove(key4_path)
                            print(f"Cleared saved passwords for Firefox profile: {profile}")
            except Exception as e:
                print(f"Error clearing Firefox passwords: {e}")
        
        elif "Opera GX Stable" in path:
            try:
                # Opera GX: ลบไฟล์ Login Data
                login_data_path = os.path.join(path, "Login Data")
                if os.path.exists(login_data_path):
                    os.remove(login_data_path)
                    print("Cleared saved passwords for Opera GX.")
            except Exception as e:
                print(f"Error clearing Opera GX passwords: {e}")
        
        else:
            # Chrome และ Edge (default)
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"Cleared stored passwords: {path}")
            except Exception as e:
                print(f"Error clearing passwords: {e}")"""

def clear_prefetch_files():
    prefetch_dir = "C:\\Windows\\Prefetch"
    if os.path.exists(prefetch_dir):
        try:
            for prefetch_file in os.listdir(prefetch_dir):
                file_path = os.path.join(prefetch_dir, prefetch_file)
                os.remove(file_path)
            print("Cleared prefetch files.")
        except Exception as e:
            print(f"Error clearing prefetch files: {e}")

def shred_file(file_path, passes=3):
    try:
        with open(file_path, "ba+", buffering=0) as file:
            length = file.tell()
            for _ in range(passes):
                file.seek(0)
                file.write(os.urandom(length))  # เขียนข้อมูลสุ่มทับไฟล์เดิม
        os.remove(file_path)  # ลบไฟล์จริง
        print(f"Shredded and deleted: {file_path}")
    except Exception as e:
        print(f"Error shredding file {file_path}: {e}")

def clear_thumbnail_cache():
    thumbnail_cache = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\Explorer")
    if os.path.exists(thumbnail_cache):
        try:
            for root, dirs, files in os.walk(thumbnail_cache):
                for file in files:
                    if file.startswith("thumbcache"):
                        os.remove(os.path.join(root, file))
            print("Cleared thumbnail cache.")
        except Exception as e:
            print(f"Error clearing thumbnail cache: {e}")

def clear_system_restore_points():
    try:
        subprocess.call(["vssadmin", "delete", "shadows", "/all", "/quiet"], shell=True)
        print("Cleared all system restore points.")
    except Exception as e:
        print(f"Error clearing system restore points: {e}")

def main():
    print("Starting full cleanup process...")
    clear_temp_files()
    clear_browser_history()
    clear_browser_downloads()
    clear_system_logs()
    clear_recent_files()
    clear_clipboard()
    #clear_cmd_powershell_history()
    #clear_browser_saved_passwords()
    clear_prefetch_files()
    #clear_remote_desktop_history()
    #clear_network_profiles()
    clear_thumbnail_cache()
    clear_registry_keys()
    clear_system_restore_points()
    disable_prefetch_superfetch()
    print("Comprehensive cleanup completed.")

if __name__ == "__main__":
    main()