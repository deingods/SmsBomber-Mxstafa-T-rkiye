from colorama import Fore, Style
from time import sleep, time
from os import system
from sms import SendSms
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkFont
from tkinter import scrolledtext
import sys
from io import StringIO
import warnings
from datetime import datetime

def servis_metotlarini_getir():
    return [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith("__")]

def temizle():
    system("cls||clear")

def get_operator(phone):
    if phone.startswith("5"):
        first_digits = phone[:3]
        if first_digits in ["501", "505", "506", "507"]:
            return "Turkcell"
        elif first_digits in ["530", "533", "536", "537"]:
            return "Vodafone"
        elif first_digits in ["541", "542", "543", "544"]:
            return "Türk Telekom"
    return "Bilinmiyor"

def loading_ekrani():
    temizle()
    colors = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
    
    ascii_art = """
    __  __ _    _  _____ _______  _      ______  _     
    |  \\/  | |  | |/ ____|__   __|/ \\    |  ____|/ \\    
    | \\  / | |  | | (___    | |  / _ \\   | |__  / _ \\   
    | |\\/| | |  | |\\___ \\   | | / ___ \\  |  __|/ ___ \\  
    | |  | | |__| |____) |  | |/ /   \\ \\ | |  / /   \\ \\ 
    |_|  |_|\\____/|_____/   |_/_/     \\_\\|_| /_/     \\_\\
    """
    
    lines = ascii_art.strip().split('\n')
    for line in lines:
        colored_line = ""
        for i, char in enumerate(line):
            colored_line += colors[i % len(colors)] + char
        print(colored_line + Style.RESET_ALL)
    
    print(Fore.LIGHTCYAN_EX + "\n MXSTAFA SMSBOMBER'A HOŞ GELDİNİZ\n")
    
    for i in range(101):
        bar_length = 40
        filled = int(bar_length * i / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        percent = i
        print(Fore.LIGHTGREEN_EX + f"\r[{bar}] {percent}%", end="", flush=True)
        sleep(0.05)
    
    print(Fore.LIGHTGREEN_EX + "\n\n Yükleme tamamlandı!\n")
    sleep(1)

def menu_secimi():
    temizle()
    colors = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
    
    ascii_art = """
    __  __ _    _  _____ _______  _      ______  _     
    |  \\/  | |  | |/ ____|__   __|/ \\    |  ____|/ \\    
    | \\  / | |  | | (___    | |  / _ \\   | |__  / _ \\   
    | |\\/| | |  | |\\___ \\   | | / ___ \\  |  __|/ ___ \\  
    | |  | | |__| |____) |  | |/ /   \\ \\ | |  / /   \\ \\ 
    |_|  |_|\\____/|_____/   |_/_/     \\_\\|_| /_/     \\_\\
    """
    
    lines = ascii_art.strip().split('\n')
    for line in lines:
        colored_line = ""
        for i, char in enumerate(line):
            colored_line += colors[i % len(colors)] + char
        print(colored_line + Style.RESET_ALL)
    
    print(Fore.LIGHTMAGENTA_EX + "\n 1- SMS Gönder (Normal)\n 2- SMS Gönder (Turbo)\n")
    return input(Fore.LIGHTYELLOW_EX + " Seçim: ")

class SMSBomberGUI:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        self.root.title("MXSTAFA SMS BOMBER - Advanced")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0d1b2a")
        self.is_running = False
        
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        warnings.filterwarnings("ignore")
        
        self.label_font = tkFont.Font(family="Courier New", size=10)
        self.button_font = tkFont.Font(family="Courier New", size=11, weight="bold")
        
        self.log_filter = "all"
        self.logs = {"success": [], "error": [], "warning": []}
        self.api_stats = {}
        self.passive_apis = set()
        self.speed_mode = "medium"
        self.dynamic_delay = 1
        
        self.setup_ui()
    
    def setup_ui(self):
        top_frame = tk.Frame(self.root, bg="#0d1b2a")
        top_frame.pack(pady=15)
        
        if self.mode == "2":
            warning_font = tkFont.Font(family="Courier New", size=12, weight="bold")
            warning_text = "Bu bomber Mxstafa tarafından yapılmıştır saygılarla DEİNGOD\nUYARI: NUMARA ARALARINDA BOŞLUK BIRAKMAYINIZ"
        else:
            warning_font = tkFont.Font(family="Courier New", size=11, weight="bold")
            warning_text = "Bu bomber Mxstafa tarafından yapılmıştır saygılarla DEİNGOD\nUYARI: NUMARALARIN ARASINDA BOSLUK BIRAKMAYINIZ CALIŞMAZ"
        
        warning_label = tk.Label(top_frame, text=warning_text, font=warning_font, 
                                bg="#0d1b2a", fg="#ff0055", justify=tk.CENTER)
        warning_label.pack()
        
        main_container = tk.Frame(self.root, bg="#0d1b2a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        left_panel = tk.Frame(main_container, bg="#0d1b2a", width=380)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Telefon numarası
        phone_frame = tk.Frame(left_panel, bg="#0d1b2a")
        phone_frame.pack(anchor="w", pady=(10, 5))
        
        phone_label = tk.Label(phone_frame, text="📱 Telefon Numarası:", font=self.label_font, bg="#0d1b2a", fg="#00d4ff")
        phone_label.pack(anchor="w")
        
        self.phone_entry = tk.Entry(phone_frame, font=self.label_font, bg="#1a2f45", fg="#00d4ff", 
                                   insertbackground="#00d4ff", width=35, relief=tk.FLAT, bd=2)
        self.phone_entry.pack(anchor="w", pady=(0, 5), ipady=8)
        
        # Operatör bilgisi sadece 1. sekmede
        if self.mode == "1":
            self.phone_entry.bind("<KeyRelease>", self.update_operator_info)
            self.operator_label = tk.Label(phone_frame, text="", font=("Courier New", 9), bg="#0d1b2a", fg="#00ff00")
            self.operator_label.pack(anchor="w")
        
        # Mail
        mail_label = tk.Label(left_panel, text="� Mail Adresi:", font=self.label_font, bg="#0d1b2a", fg="#00d4ff")
        mail_label.pack(anchor="w", pady=(15, 5))
        
        self.mail_entry = tk.Entry(left_panel, font=self.label_font, bg="#1a2f45", fg="#00d4ff", 
                                  insertbackground="#00d4ff", width=35, relief=tk.FLAT, bd=2)
        self.mail_entry.pack(anchor="w", pady=(0, 15), ipady=8)
        
        # SMS Sayısı
        count_label = tk.Label(left_panel, text="📊 SMS Sayısı:", font=self.label_font, bg="#0d1b2a", fg="#00d4ff")
        count_label.pack(anchor="w", pady=(10, 5))
        
        self.count_entry = tk.Entry(left_panel, font=self.label_font, bg="#1a2f45", fg="#00d4ff", 
                                   insertbackground="#00d4ff", width=35, relief=tk.FLAT, bd=2)
        self.count_entry.pack(anchor="w", pady=(0, 15), ipady=8)
        
        # Slider sadece 1. sekmede
        if self.mode == "1":
            speed_label = tk.Label(left_panel, text="⚡ Test Hızı:", font=self.label_font, bg="#0d1b2a", fg="#00d4ff")
            speed_label.pack(anchor="w", pady=(10, 5))
            
            speed_frame = tk.Frame(left_panel, bg="#0d1b2a")
            speed_frame.pack(anchor="w", pady=(0, 15))
            
            tk.Label(speed_frame, text="Yavaş", font=("Courier New", 8), bg="#0d1b2a", fg="#00d4ff").pack(side=tk.LEFT, padx=5)
            
            self.speed_slider = tk.Scale(speed_frame, from_=1, to=3, orient=tk.HORIZONTAL, 
                                         bg="#1a2f45", fg="#00d4ff", troughcolor="#0a1420",
                                         command=self.update_speed_mode, relief=tk.FLAT, bd=0, length=200)
            self.speed_slider.set(2)
            self.speed_slider.pack(side=tk.LEFT, padx=5)
            
            tk.Label(speed_frame, text="Agresif", font=("Courier New", 8), bg="#0d1b2a", fg="#00d4ff").pack(side=tk.LEFT, padx=5)
            
            self.speed_mode_label = tk.Label(left_panel, text="Mod: Orta", font=("Courier New", 9), bg="#0d1b2a", fg="#ffff00")
            self.speed_mode_label.pack(anchor="w", pady=(0, 15))
        else:
            self.speed_slider = None
            self.speed_mode_label = None
        
        # Butonlar
        button_frame = tk.Frame(left_panel, bg="#0d1b2a")
        button_frame.pack(fill=tk.X, pady=20)
        
        self.start_btn = tk.Button(button_frame, text="� BAŞLAT", font=self.button_font, 
                                   bg="#ff0055", fg="white", activebackground="#ff3377", activeforeground="white",
                                   command=self.start_attack, relief=tk.FLAT, padx=25, pady=12, cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="⏹️  DURDUR", font=self.button_font,
                                  bg="#333333", fg="#888888", activebackground="#444444", activeforeground="#aaaaaa",
                                  command=self.stop_attack, relief=tk.FLAT, padx=25, pady=12, cursor="hand2", state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(left_panel, text="💾 Raporu Kaydet", font=self.button_font,
                 bg="#1a2f45", fg="#00d4ff", command=self.save_report, relief=tk.FLAT, padx=20, pady=10, cursor="hand2").pack(fill=tk.X, pady=10)
        
        # Sağ panel - Terminal Log
        right_panel = tk.Frame(main_container, bg="#0d1b2a")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        filter_frame = tk.Frame(right_panel, bg="#0d1b2a")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(filter_frame, text="Tümünü Gör", font=("Courier New", 9), bg="#1a2f45", fg="#00d4ff",
                 command=lambda: self.set_filter("all"), relief=tk.FLAT, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(filter_frame, text="✓ Başarılı", font=("Courier New", 9), bg="#1a2f45", fg="#00ff00",
                 command=lambda: self.set_filter("success"), relief=tk.FLAT, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(filter_frame, text="✗ Hatalı", font=("Courier New", 9), bg="#1a2f45", fg="#ff0055",
                 command=lambda: self.set_filter("error"), relief=tk.FLAT, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(filter_frame, text="! Şüpheli", font=("Courier New", 9), bg="#1a2f45", fg="#ffff00",
                 command=lambda: self.set_filter("warning"), relief=tk.FLAT, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        log_label = tk.Label(right_panel, text="📋 Terminal Log", font=("Courier New", 11, "bold"), 
                            bg="#0d1b2a", fg="#00d4ff")
        log_label.pack(anchor="w", pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(right_panel, font=("Courier New", 9), 
                                                 bg="#0a1420", fg="#00ff00", relief=tk.FLAT, bd=0,
                                                 wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        self.log_text.tag_config("success", foreground="#00ff00")
        self.log_text.tag_config("error", foreground="#ff0055")
        self.log_text.tag_config("warning", foreground="#ffff00")
        
        status_frame = tk.Frame(self.root, bg="#1a2f45", relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, text="✓ Hazır", font=self.label_font, bg="#1a2f45", fg="#00d4ff")
        self.status_label.pack(anchor="w", padx=10, pady=5)
    
    def update_operator_info(self, event=None):
        phone = self.phone_entry.get().strip()
        if len(phone) == 10 and phone.isdigit():
            operator = get_operator(phone)
            self.operator_label.config(text=f"✓ {operator}", fg="#00ff00")
        else:
            self.operator_label.config(text="")
    
    def update_speed_mode(self, value):
        value = int(value)
        if value == 1:
            self.speed_mode = "slow"
            self.speed_mode_label.config(text="Mod: Yavaş (3s)")
            self.dynamic_delay = 3
        elif value == 2:
            self.speed_mode = "medium"
            self.speed_mode_label.config(text="Mod: Orta (1s)")
            self.dynamic_delay = 1
        else:
            self.speed_mode = "aggressive"
            self.speed_mode_label.config(text="Mod: Agresif (Dinamik)")
            self.dynamic_delay = 0.5
    
    def set_filter(self, filter_type):
        self.log_filter = filter_type
        self.refresh_log()
    
    def refresh_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        if self.log_filter == "all":
            logs = self.logs["success"] + self.logs["error"] + self.logs["warning"]
        elif self.log_filter == "success":
            logs = self.logs["success"]
        elif self.log_filter == "error":
            logs = self.logs["error"]
        else:
            logs = self.logs["warning"]
        
        for log_entry in logs:
            self.log_text.insert(tk.END, log_entry["text"], log_entry["tag"])
        
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def log_message(self, message, status="success", error_code=None):
        if status == "success":
            text = f"✓ {message}\n"
            tag = "success"
            self.logs["success"].append({"text": text, "tag": tag})
        elif status == "error":
            error_info = f" [{error_code}]" if error_code else ""
            text = f"✗ {message}{error_info}\n"
            tag = "error"
            self.logs["error"].append({"text": text, "tag": tag})
        else:
            text = f"! {message}\n"
            tag = "warning"
            self.logs["warning"].append({"text": text, "tag": tag})
        
        if self.log_filter == "all" or (self.log_filter == "success" and status == "success") or \
           (self.log_filter == "error" and status == "error") or (self.log_filter == "warning" and status == "warning"):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, text, tag)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        
        self.root.update()
    
    def save_report(self):
        if not self.logs["success"] and not self.logs["error"]:
            messagebox.showwarning("Uyarı", "Henüz rapor kaydedecek veri yok!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if not file_path:
            return
        
        success_count = len(self.logs["success"])
        error_count = len(self.logs["error"])
        warning_count = len(self.logs["warning"])
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MXSTAFA SMS Bomber Raporu</title>
    <style>
        body {{ background: #0d1b2a; color: #00d4ff; font-family: 'Courier New'; margin: 20px; }}
        .header {{ text-align: center; color: #ff0055; font-size: 24px; margin-bottom: 30px; }}
        .stats {{ display: flex; justify-content: space-around; margin-bottom: 30px; }}
        .stat-box {{ background: #1a2f45; padding: 20px; border-radius: 5px; text-align: center; }}
        .success {{ color: #00ff00; }}
        .error {{ color: #ff0055; }}
        .warning {{ color: #ffff00; }}
    </style>
</head>
<body>
    <div class="header">🚀 MXSTAFA SMS BOMBER RAPORU</div>
    <div class="stats">
        <div class="stat-box"><div class="success">✓ Başarılı: {success_count}</div></div>
        <div class="stat-box"><div class="error">✗ Hatalı: {error_count}</div></div>
        <div class="stat-box"><div class="warning">! Şüpheli: {warning_count}</div></div>
    </div>
    <p style="text-align: center; margin-top: 30px; color: #888;">Rapor: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body>
</html>"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        messagebox.showinfo("Başarılı", f"Rapor kaydedildi!")
    
    def start_attack(self):
        phone = self.phone_entry.get().strip()
        mail = self.mail_entry.get().strip()
        
        if not phone or len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Hata", "Geçerli bir telefon numarası giriniz!")
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🔴 Saldırı Başladı...", fg="#ff0055")
        
        self.logs = {"success": [], "error": [], "warning": []}
        self.api_stats = {}
        self.passive_apis = set()
        self.refresh_log()
        
        self.log_message(f"Hedef: +90{phone} ({get_operator(phone)})", "success")
        self.log_message("Saldırı başlatılıyor...", "success")
        
        threading.Thread(target=self.attack_thread, args=(phone, mail), daemon=True).start()
    
    def attack_thread(self, phone, mail):
        try:
            sms = SendSms(phone, mail)
            count = 0
            
            try:
                count_input = self.count_entry.get().strip()
                max_count = int(count_input) if count_input else None
            except ValueError:
                self.log_message("Geçerli bir sayı giriniz!", "error", "INPUT_ERROR")
                self.stop_attack()
                return
            
            # 1. sekmede slider kullan, 2. sekmede turbo (aralık 0)
            if self.mode == "1":
                delay = self.dynamic_delay
            else:
                delay = 0  # Turbo mode
            
            if self.mode == "1":
                while self.is_running:
                    for method in servis_metotlarini_getir():
                        if not self.is_running or method in self.passive_apis:
                            continue
                        
                        try:
                            getattr(sms, method)()
                            count += 1
                            
                            if method not in self.api_stats:
                                self.api_stats[method] = {"success": 0, "fail": 0}
                            self.api_stats[method]["success"] += 1
                            
                            self.status_label.config(text=f"📤 Gönderilen: {count}", fg="#00d4ff")
                            self.log_message(f"SMS #{count} gönderildi ({method})", "success")
                            
                            if max_count and count >= max_count:
                                self.is_running = False
                                break
                            
                            sleep(delay)
                        except Exception as e:
                            error_msg = str(e)
                            error_code = "TIMEOUT" if "timeout" in error_msg.lower() else \
                                        "RATE_LIMIT" if "rate" in error_msg.lower() or "429" in error_msg else \
                                        "API_DOWN" if "connection" in error_msg.lower() or "503" in error_msg else "UNKNOWN"
                            
                            if method not in self.api_stats:
                                self.api_stats[method] = {"success": 0, "fail": 0}
                            self.api_stats[method]["fail"] += 1
                            
                            if self.api_stats[method]["fail"] >= 3:
                                self.passive_apis.add(method)
                                self.log_message(f"API Beklemede ({method})", "warning")
                            else:
                                self.log_message(f"SMS gönderimi başarısız ({method})", "error", error_code)
                                
                                if self.speed_mode == "aggressive" and error_code == "RATE_LIMIT":
                                    self.dynamic_delay = min(self.dynamic_delay + 1, 5)
                    
                    if max_count and count >= max_count:
                        break
            
            elif self.mode == "2":
                while self.is_running:
                    threadler = []
                    for method in servis_metotlarini_getir():
                        if not self.is_running or method in self.passive_apis:
                            continue
                        
                        t = threading.Thread(target=self.send_sms_thread, args=(sms, method, count), daemon=True)
                        threadler.append(t)
                        t.start()
                        count += 1
                        self.status_label.config(text=f"📤 Gönderilen: {count}", fg="#00d4ff")
                        
                        if max_count and count >= max_count:
                            self.is_running = False
                            break
                    
                    for t in threadler:
                        t.join()
                    
                    if max_count and count >= max_count:
                        break
        
        except Exception as e:
            self.log_message(f"Kritik Hata: {str(e)}", "error", "CRITICAL")
        finally:
            self.stop_attack()
    
    def send_sms_thread(self, sms, method, count):
        try:
            getattr(sms, method)()
            if method not in self.api_stats:
                self.api_stats[method] = {"success": 0, "fail": 0}
            self.api_stats[method]["success"] += 1
            self.log_message(f"SMS #{count} gönderildi ({method})", "success")
        except Exception as e:
            error_code = "TIMEOUT" if "timeout" in str(e).lower() else \
                        "RATE_LIMIT" if "rate" in str(e).lower() or "429" in str(e) else \
                        "API_DOWN" if "connection" in str(e).lower() or "503" in str(e) else "UNKNOWN"
            
            if method not in self.api_stats:
                self.api_stats[method] = {"success": 0, "fail": 0}
            self.api_stats[method]["fail"] += 1
            
            if self.api_stats[method]["fail"] >= 3:
                self.passive_apis.add(method)
                self.log_message(f"API Beklemede ({method})", "warning")
            else:
                self.log_message(f"SMS gönderimi başarısız ({method})", "error", error_code)
    
    def stop_attack(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="✓ Durduruldu", fg="#00d4ff")
        self.log_message("Saldırı durduruldu.", "success")

def main():
    loading_ekrani()
    
    while True:
        secim = menu_secimi()
        
        if secim == "1" or secim == "2":
            root = tk.Tk()
            app = SMSBomberGUI(root, secim)
            root.mainloop()
        else:
            temizle()
            print(Fore.LIGHTRED_EX + "Geçersiz seçim. Tekrar deneyiniz.")
            sleep(2)

if __name__ == "__main__":
    main()
