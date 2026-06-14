# data/bin/launcher.py
import ctypes
import sys
import subprocess
import os

def is_admin() -> bool:
    """检查当前脚本是否拥有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """如果当前没有管理员权限，则通过UAC重新启动脚本"""
    if is_admin():
        return
    # 重新运行当前脚本并请求管理员权限
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

def run_installer() -> bool:
    """启动 Lockhead.exe 安装程序，必要时刻请求管理员权限"""
    # 如果当前脚本没有管理员权限，则请求权限并重新运行
    run_as_admin()

    # 获取安装程序路径
    current_dir = os.path.dirname(__file__)
    exe_path = os.path.join(current_dir, "Lockhead.exe")

    if not os.path.exists(exe_path):
        print(f"错误：在 {exe_path} 未找到安装程序。")
        return False

    try:
        # 使用 subprocess.Popen 启动安装程序
        if sys.platform == "win32":
            subprocess.Popen([exe_path], shell=True)
        else:
            subprocess.Popen([exe_path])
        return True
    except Exception as e:
        print(f"启动安装程序失败：{e}")
        return False
