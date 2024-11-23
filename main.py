import ctypes
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime, timedelta
import pytz
import random
import pygame
from plyer import notification
import time
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# Initialize global variables
running = False
start_time = 0
elapsed_time = 0
alarm_time = None

# Initialize pygame mixer
pygame.mixer.init()

# Ringtones
ringtones = [
    "barbie_jiafei.mp3",
    "jiafei_irl.mp3",
    "jiafei_samsung.mp3",
    "rapgod_jiafei.mp3",
    "stop_it_jiafei.mp3",
    "symphony_jiafei.mp3",
    "the_little_product.mp3",
    "under_the_sea_jiafei.mp3"
]

# Create the main window
root = tk.Tk()
root.title("Bestie Alarm Clock")
root.geometry("900x600")
root.configure(background="#FFA3DA")

font_style = ("Mochiy Pop One", 15)

# Set System-Wide Maximum Volume
def set_max_volume_system():
    ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)  # Increase volume key
    for _ in range(50):  # Send the key event 50 times to ensure max volume
        ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)

# Stopwatch Functions
def update_time():
    if running:
        global elapsed_time
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        main_label.config(text=formatted_time)
        root.after(100, update_time)

def start_stopwatch():
    global running, start_time
    if running:
        btn_stopwatch.config(text="Start Stopwatch")
        running = False
        btn_cancel.place_forget()
    else:
        btn_stopwatch.config(text="Pause Stopwatch")
        start_time = time.time() - elapsed_time
        running = True
        update_time()
        btn_cancel.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

def cancel():
    global running, start_time, elapsed_time
    running = False
    start_time = 0
    elapsed_time = 0
    main_label.config(text="00:00:00")
    btn_stopwatch.config(text="Start Stopwatch")
    btn_cancel.place_forget()

# Timer Functions
def start_timer():
    def set_timer():
        nonlocal timer_window
        try:
            total_seconds = int(entry_seconds.get() or 0) + \
                            int(entry_minutes.get() or 0) * 60 + \
                            int(entry_hours.get() or 0) * 3600
            if total_seconds > 0:
                timer_window.destroy()
                countdown(total_seconds)
            else:
                main_label.config(text="Invalid Time!")
        except ValueError:
            main_label.config(text="Enter numbers only!")

    timer_window = tk.Toplevel(root)
    timer_window.title("Set Timer")
    timer_window.geometry("400x300")
    timer_window.configure(background="#FFA3DA")

    tk.Label(timer_window, text="Hours:", bg="#FFA3DA", font=font_style).pack(pady=5)
    entry_hours = tk.Entry(timer_window, font=font_style)
    entry_hours.pack()

    tk.Label(timer_window, text="Minutes:", bg="#FFA3DA", font=font_style).pack(pady=5)
    entry_minutes = tk.Entry(timer_window, font=font_style)
    entry_minutes.pack()

    tk.Label(timer_window, text="Seconds:", bg="#FFA3DA", font=font_style).pack(pady=5)
    entry_seconds = tk.Entry(timer_window, font=font_style)
    entry_seconds.pack()

    tk.Button(timer_window, text="Set Timer", bg="#FD71C5", font=font_style, command=set_timer).pack(pady=10)

def countdown(seconds):
    global running
    if not running:
        running = True
    if seconds > 0:
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        main_label.config(text=f"{hours:02}:{minutes:02}:{secs:02}", font=("Mochiy Pop One", 80))
        root.after(1000, countdown, seconds - 1)
    else:
        running = False
        main_label.config(text="I <3 Diddy Parties", font=("Mochiy Pop One", 60))
        selected_ringtone = random.choice(ringtones)
        play_ringtone(selected_ringtone)
        notification.notify(title="Time's Up BBG", message="Time's Up My Puchaina😩🔥💀😭🙏", timeout=10)

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Alarm Functions
def set_alarm():
    global alarm_time

    alarm_window = tk.Toplevel(root)
    alarm_window.title("Set Alarm")
    alarm_window.geometry("400x200")
    alarm_window.configure(background="#FFA3DA")

    tk.Label(alarm_window, text="Set Alarm Time", bg="#FFA3DA", font=font_style).pack(pady=10)

    hour_var = tk.StringVar(value="00")
    minute_var = tk.StringVar(value="00")
    second_var = tk.StringVar(value="00")
    period_var = tk.StringVar(value="AM")

    tk.Entry(alarm_window, textvariable=hour_var, font=font_style, width=2).pack(side=tk.LEFT, padx=5)
    tk.Label(alarm_window, text=":", bg="#FFA3DA", font=font_style).pack(side=tk.LEFT)
    tk.Entry(alarm_window, textvariable=minute_var, font=font_style, width=2).pack(side=tk.LEFT, padx=5)
    tk.Label(alarm_window, text=":", bg="#FFA3DA", font=font_style).pack(side=tk.LEFT)
    tk.Entry(alarm_window, textvariable=second_var, font=font_style, width=2).pack(side=tk.LEFT, padx=5)

    tk.OptionMenu(alarm_window, period_var, "AM", "PM").pack(side=tk.LEFT, padx=5)

    def save_alarm():
        global alarm_time
        try:
            time_str = f"{hour_var.get()}:{minute_var.get()}:{second_var.get()} {period_var.get()}"
            alarm_time_obj = datetime.strptime(time_str, "%I:%M:%S %p").time()
            alarm_time = alarm_time_obj
            print(f"Set alarm for {alarm_time}")
            alarm_window.destroy()
            check_alarm_time()
        except ValueError:
            print("Invalid time format. Please check your input.")

    tk.Button(alarm_window, text="Set Alarm", font=font_style, bg="#FD71C5", command=save_alarm).pack(pady=10)

def check_alarm_time():
    global alarm_time
    if alarm_time:
        nz_time = datetime.now(pytz.timezone('Pacific/Auckland')).time()
        if nz_time >= alarm_time:
            main_label.config(text="Wake Up Bestie🤞")
            selected_ringtone = random.choice(ringtones)
            play_ringtone(selected_ringtone)
            notification.notify(title="Wake Up BBG", message="Jiafei Is Calling Pookie Wake Up😭", timeout=10)
            alarm_time = None
        else:
            root.after(1000, check_alarm_time)

def play_ringtone(ringtone_path):
    set_max_volume_system()  # Set volume to maximum
    play_sound(ringtone_path)  # Play the sound

# UI Elements
label = tk.Label(root, text="bestie alarm clock", font=("Mochiy Pop One", 40), bg="#FFA3DA")
main_label = tk.Label(root, font=("Mochiy Pop One", 80), bg="#FFA3DA")
footer_label = tk.Label(root, text="The Preppiest Alarm Clock", font=("Mochiy Pop One", 10), bg="#FFA3DA", fg="#FD71C5")

label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
main_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
footer_label.place(relx=0.5, rely=0.97, anchor=tk.CENTER)

btn_stopwatch = tk.Button(root, text="Start Stopwatch", font=font_style, bg="#FD71C5", command=start_stopwatch)
btn_stopwatch.place(relx=0.2, rely=0.8, anchor=tk.CENTER)

btn_timer = tk.Button(root, text="Set Timer", font=font_style, bg="#FD71C5", command=start_timer)
btn_timer.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

btn_alarm = tk.Button(root, text="Set Alarm", font=font_style, bg="#FD71C5", command=set_alarm)
btn_alarm.place(relx=0.8, rely=0.8, anchor=tk.CENTER)

btn_cancel = tk.Button(root, text="Cancel", font=font_style, bg="#FFA3DA", command=cancel)
btn_cancel.place_forget()

root.mainloop()
