# =====================================================================
# ULTIMATE SYSTEM SENTINEL ENGINE (LEVEL 2: AUTONOMOUS DAEMON)
# Developed under Master-Student Protocol
# =====================================================================

import psutil
import time
import os
import datetime

class AutonomousSentinel:
    def __init__(self, memory_threshold_mb=350, check_interval_sec=5):
        self.memory_threshold = memory_threshold_mb * 1024 * 1024  # Bytes
        self.interval = check_interval_sec
        self.log_file = "sentinel_audit.log"
        print("🛡️ [AUTONOMOUS SENTINEL v2.0] INITIALIZED...")
        print("⚡ Mode: Active Kernel & Memory Defense Daemon")
        print(f"🎯 Threshold: {memory_threshold_mb} MB | Interval: {check_interval_sec}s\n")

    def write_log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def run_daemon(self):
        print("🔄 Sentinel Daemon is now running in background... Press Ctrl+C to abort.")
        try:
            while True:
                threats_found = False
                for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                    try:
                        mem_usage = proc.info['memory_info'].rss
                        
                        if mem_usage > self.memory_threshold:
                            pid = proc.info['pid']
                            name = proc.info['name']
                            mem_mb = round(mem_usage / (1024 * 1024), 2)
                            
                            if name in ['system_server', 'zygote', 'com.termux']:
                                continue
                                
                            threats_found = True
                            print(f"\n⚠️ ANOMALY DETECTED! PID: {pid} | Name: {name} | Usage: {mem_mb} MB")
                            
                            p = psutil.Process(pid)
                            p.terminate()
                            
                            alert_msg = f"NEUTRALIZED -> PID: {pid}, Name: {name}, Memory: {mem_mb} MB"
                            print(f"⚡ ACTION: {alert_msg}")
                            self.write_log(alert_msg)
                            
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                
                if not threats_found:
                    print(".", end="", flush=True)
                    
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Sentinel Daemon manually stopped by Master.")


if __name__ == "__main__":
    sentinel = AutonomousSentinel(memory_threshold_mb=300, check_interval_sec=5)
    sentinel.run_daemon()
# =====================================================================
# ULTIMATE SYSTEM SENTINEL ENGINE (LEVEL 1)
# Developed under Master-Student Protocol
# =====================================================================

import psutil
import time
import os

class SystemSentinel:
    def __init__(self, memory_threshold_mb=300):
        self.memory_threshold = memory_threshold_mb * 1024 * 1024  # Bytes
        print("🛡️ SENTINEL ENGINE INITIALIZED: Monitoring Kernel & User Space Processes...")

    def scan_suspicious_processes(self):
        """
        সিস্টেমে চলা প্রতিটি প্রসেসের মেমোরি ও আচরণ স্ক্যান করা
        """
        print("\n🔍 Scanning system processes for anomalous memory usage...")
        flagged_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                # প্রসেসের মেমোরি ব্যবহারের তথ্য নেওয়া
                mem_usage = proc.info['memory_info'].rss
                
                # অস্বাভাবিক মেমোরি ইউসেজ হলে প্রসেস ফ্লেগ করা
                if mem_usage > self.memory_threshold:
                    flagged_processes.append({
                        'PID': proc.info['pid'],
                        'Name': proc.info['name'],
                        'Memory_MB': round(mem_usage / (1024 * 1024), 2)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return flagged_processes

    def neutralize_threat(self, pid):
        """
        টার্গেট প্রসেসকে সিস্টেমে টার্মিনেট/ধ্বংস করে দেওয়া
        """
        try:
            p = psutil.Process(pid)
            p.terminate()  # প্রসেস বন্ধ করার কমান্ড
            print(f"⚡ SUCCESS: Process PID {pid} has been NEUTRALIZED!")
        except Exception as e:
            print(f"❌ FAILED to terminate PID {pid}: {e}")

# --- মাস্টার এক্সিকিউশন ---
if __name__ == "__main__":
    print("==================================================")
    print("      CORE SECURITY SENTINEL PROTOCOL v1.0        ")
    print("==================================================")
    
    # ৫০০ মেগাবাইটের বেশি মেমোরি খাওয়া প্রসেস স্ক্যান করবে
    sentinel = SystemSentinel(memory_threshold_mb=300)
    
    threats = sentinel.scan_suspicious_processes()
    
    if threats:
        print(f"\n⚠️ WARNING: {len(threats)} Suspicious High-Memory Processes Found!")
        for threat in threats:
            print(f"-> PID: {threat['PID']} | Name: {threat['Name']} | Memory: {threat['Memory_MB']} MB")
        
        action = input("\nআপনি কি কোনো প্রসেস নিউট্রালাইজ/বন্ধ করতে চান? (PID দিন / 0 দিয়ে স্কিপ করুন): ")
        if action != '0' and action.isdigit():
            sentinel.neutralize_threat(int(action))
    else:
        print("✅ SYSTEM CLEAN: No anomalous processes detected.")

