# gui.py
import tkinter as tk
from tkinter import ttk
import webbrowser
import yaml

class FakeOBSPluginGUI:
    """Fake OBS plugin configuration window that actually warns against cheats."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DeltaForce OBS Lockhead Plugin v2.6")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Load configuration
        with open("config.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        
        # Fake settings widgets
        ttk.Label(root, text="瞄准模式:").pack(pady=5)
        self.aim_mode = ttk.Combobox(root, values=["自动压枪", "头部优先", "胸部优先"])
        self.aim_mode.pack()
        self.aim_mode.current(0)
        
        ttk.Label(root, text="平滑度:").pack(pady=5)
        self.smoothness = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.smoothness.pack()
        self.smoothness.set(50)
        
        ttk.Label(root, text="触发按键:").pack(pady=5)
        self.hotkey = ttk.Entry(root)
        self.hotkey.pack()
        self.hotkey.insert(0, "鼠标侧键")
        
        # Apply button – triggers the warning
        self.apply_btn = ttk.Button(root, text="应用并注入", command=self.on_apply)
        self.apply_btn.pack(pady=20)
        
        # Fake status bar
        self.status = ttk.Label(root, text="就绪 - 等待游戏进程")
        self.status.pack(side=tk.BOTTOM, pady=10)
    
    def on_apply(self):
        """Callback when user clicks 'Apply and Inject'."""
        self.status.config(text="正在检测游戏...")
        # Simulate detection delay
        self.root.after(1000, self.show_warning)
    
    def show_warning(self):
        """Display the anti-cheat warning and redirect to promoted game."""
        import webbrowser
        from tkinter import messagebox
        
        self.status.config(text="检测到非法外挂行为！")
        result = messagebox.askyesno(
            title=self.config['warning_message']['title'],
            message=self.config['warning_message']['text'],
            icon='warning'
        )
        if result:
            webbrowser.open(self.config['target_game']['download_page'])
            messagebox.showinfo("提示", "拒绝外挂，健康游戏。")
            self.status.config(text="已重定向至官网")
        else:
            messagebox.showwarning("风险提示", "外挂使用者将被封号，请立即卸载本插件。")
            self.status.config(text="警告：外挂使用风险自负")
        
        # Disable all interactive widgets to simulate plugin failure
        for child in self.root.winfo_children():
            if isinstance(child, (ttk.Button, ttk.Combobox, tk.Scale, ttk.Entry)):
                child.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = FakeOBSPluginGUI(root)
    root.mainloop()
