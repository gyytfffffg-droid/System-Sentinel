from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import threading
import psutil
import time
import datetime
import os

class SystemSentinelApp(App):
    def build(self):
        self.running = False
        
        # UI Layout Design
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        self.title_label = Label(text="🛡️ SYSTEM SENTINEL", font_size=24, color=(0, 1, 1, 1))
        layout.add_widget(self.title_label)
        
        self.status_label = Label(text="Status: DEFENSER IDLE", font_size=18, color=(1, 0.5, 0, 1))
        layout.add_widget(self.status_label)
        
        self.toggle_btn = Button(
            text="START SENTINEL DAEMON", 
            font_size=18, 
            background_color=(0.1, 0.7, 0.3, 1)
        )
        self.toggle_btn.bind(on_press=self.toggle_sentinel)
        layout.add_widget(self.toggle_btn)
        
        return layout

    def toggle_sentinel(self, instance):
        if not self.running:
            self.running = True
            self.status_label.text = "Status: RUNNING & PROTECTING ⚡"
            self.status_label.color = (0, 1, 0, 1)
            self.toggle_btn.text = "STOP SENTINEL"
            self.toggle_btn.background_color = (0.8, 0.1, 0.1, 1)
            
            # Run daemon in background thread so app doesn't freeze
            threading.Thread(target=self.run_daemon, daemon=True).start()
        else:
            self.running = False
            self.status_label.text = "Status: STOPPED"
            self.status_label.color = (1, 0.5, 0, 1)
            self.toggle_btn.text = "START SENTINEL DAEMON"
            self.toggle_btn.background_color = (0.1, 0.7, 0.3, 1)

    def run_daemon(self):
        memory_threshold_mb = 300
        threshold_bytes = memory_threshold_mb * 1024 * 1024
        log_file = "sentinel_audit.log"
        
        while self.running:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                    if not self.running:
                        break
                    try:
                        mem_usage = proc.info['memory_info'].rss
                        if mem_usage > threshold_bytes:
                            pid = proc.info['pid']
                            name = proc.info['name']
                            
                            if name in ['system_server', 'zygote', 'com.termux']:
                                continue
                                
                            p = psutil.Process(pid)
                            p.terminate()
                            
                            # Write log
                            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            with open(log_file, "a") as f:
                                f.write(f"[{timestamp}] NEUTRALIZED -> PID: {pid}, Name: {name}\n")
                    except:
                        pass
            except:
                pass
            time.sleep(5)

if __name__ == '__main__':
    SystemSentinelApp().run()

