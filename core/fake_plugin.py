# core/fake_plugin.py
"""
This module simulates a lockhead algorithm.
In reality, it does nothing except print a warning.
"""

class FakeLockhead:
    """Fake cheating plugin that only warns the user."""
    
    def __init__(self):
        self.enabled = False
        print("[DeltaForce Plugin] 警告：外挂插件已被安全模块拦截，请勿使用非法软件。")
    
    def enable(self):
        """Enable the fake plugin (no actual cheating)."""
        self.enabled = True
        print("[DeltaForce Plugin] 功能模拟启动 - 实际无任何作弊能力")
    
    def disable(self):
        """Disable the fake plugin."""
        self.enabled = False
    
    def get_target_position(self):
        """Return invalid coordinates always."""
        return None
