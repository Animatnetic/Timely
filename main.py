"""
Clock app, if you see this, then I chose to make it open source.
Uses ttkboostrapped tkinter for practice of my problem-solving
Not a single Youtube tutorial has been used for the main functionalities of the app itself (simply reading
online forums and stackoverflow posts for certain mild problems)

A way of escaping tutorial hell I guess, and making a project I actually am really proud for
Anyway, certainly helped my problem-solving and was fun to do.

I guess upping my skills in Tkinter were not so bad after all as I now find dealing with design of UI not AS BAD
"""

from PIL import Image, ImageTk

import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from datetime import datetime
from playsound import playsound
import os
import sys


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# Followed resource_path function has been derived from above stack overflow thread as to help make the py file into one file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class TimeFrame(ttb.Frame):
    def __init__(self, master):
        self.selector = ttb.Frame(master)

        now_time = datetime.now()
        string_time = now_time.strftime("%H : %M : %S")

        self.time_label = ttb.Label(self.selector, text=string_time,
                                    font=("Arial Greek", 32, "bold"), bootstyle=INFO)
        self.time_label.grid(row=1, column=0, padx=100)

        self.update_time()

    def update_time(self):
        new_time = datetime.now()
        new_string_time = new_time.strftime("%H : %M : %S")

        self.time_label.config(text=new_string_time)
        self.selector.after(1000, self.update_time)


class TimerFrame(ttb.Frame):
    def __init__(self, master):
        def format_time(seconds: int):
            hours, seconds_remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds_remainder, 60)

            return f"{hours:02d} : {minutes:02d} : {seconds:02d}"

        def update_timer():
            alarm_activated = False

            if not alarm_activated:
                self.time_in_seconds -= 1
            self.timer_meter.configure(amountused=self.time_in_seconds)

            self.updated_stringified_time = format_time(self.time_in_seconds)
            self.timer_tick.config(text=self.updated_stringified_time)

            if self.time_in_seconds == 0:
                alarm_activated = True

            self.timer_afterfunc_id = self.selector.after(1000, lambda: allow_update_timer(alarm_activated))

        def alarm():
            def play_alarm_sound():
                playsound(resource_path("alarm_sound.wav"), block=False)

            self.cancel_button.configure(text="Stop")
            self.pause_button.grid_forget()
            self.cancel_button.grid(row=0, column=1, sticky=N, padx=0, pady=10)
            self.timer_tick.configure(bootstyle=WARNING)
            self.timer_meter.configure(amountused=self.totalling_time, bootstyle=WARNING)

            play_alarm_sound()
            self.alarm_afterfunc_id = self.selector.after(1000, alarm)

        def allow_update_timer(activated):
            if not activated:
                update_timer()
            else:
                alarm()

        def pause_timer():
            self.selector.after_cancel(self.timer_afterfunc_id)
            self.pause_button.configure(text="Continue", bootstyle=SUCCESS, command=update_pause)

        def update_pause():
            self.pause_button.configure(text="Pause", bootstyle=WARNING, command=pause_timer)
            self.time_in_seconds += 1
            update_timer()

        def cancel_timer():
            self.selector.after_cancel(self.timer_afterfunc_id)
            self.activated_timer_frame.destroy()
            self.timer_entry_frame.grid(row=0, columnspan=3, padx=50)
            self.start_timer_btn.grid(row=1, column=1, padx=50, pady=50)

        def start_timer():
            hours_entry_val = self.hours_entry.get()
            minutes_entry_val = self.minutes_entry.get()
            seconds_entry_val = self.seconds_entry.get()

            if hours_entry_val == "" and minutes_entry_val == "" and seconds_entry_val == "":
                pass
            else:
                try:
                    entry_values = [hours_entry_val, minutes_entry_val, seconds_entry_val]

                    for value_index in range(len(entry_values)):
                        if entry_values[value_index] == "":
                            if value_index == 0:
                                hours_entry_val = 0
                            elif value_index == 1:
                                minutes_entry_val = 0
                            elif value_index == 2:
                                seconds_entry_val = 0

                    int(hours_entry_val)  # Type check
                    int(minutes_entry_val)  # Type check
                    int(seconds_entry_val)  # Type checks

                    print(hours_entry_val, minutes_entry_val, seconds_entry_val)

                    self.timer_entry_frame.grid_forget()
                    self.start_timer_btn.grid_forget()

                    self.time_in_seconds = (int(hours_entry_val) * 3600) + (int(minutes_entry_val) * 60) + (
                        int(seconds_entry_val))
                    self.totalling_time = self.time_in_seconds
                    self.stringify_time = format_time(self.time_in_seconds)

                    self.activated_timer_frame = ttb.Frame(self.selector)

                    self.pause_button = ttb.Button(self.activated_timer_frame, text="Pause",
                                                   bootstyle="warning-outline", command=pause_timer)
                    self.pause_button.grid(row=0, column=1, sticky="NE")

                    self.cancel_button = ttb.Button(self.activated_timer_frame, text="Cancel",
                                                    bootstyle="danger-outline", command=cancel_timer)
                    self.cancel_button.grid(row=0, column=1, sticky="NW", padx=5)

                    self.timer_meter = ttb.Meter(self.activated_timer_frame, interactive=False,
                                                 amountused=self.time_in_seconds, showtext=False,
                                                 metersize=250, amounttotal=self.totalling_time)
                    self.timer_tick = ttb.Label(self.timer_meter, text=self.stringify_time,
                                                font=("Arial Greek", 20, "bold"))
                    self.timer_meter.grid(row=1, column=1, padx=85)
                    self.timer_tick.pack(side="top")

                    self.activated_timer_frame.grid(row=0, column=0)
                    self.selector.after(1000, update_timer)
                except ValueError:
                    return None

        self.selector = ttb.Frame(master)

        self.timer_entry_frame = ttb.Frame(self.selector)
        self.divider = ttb.Label(self.timer_entry_frame, text=":", font=("Arial Greek", 20, "bold"), bootstyle=LIGHT)
        self.divider2 = ttb.Label(self.timer_entry_frame, text=":", font=("Arial Greek", 20, "bold"), bootstyle=LIGHT)

        self.hours_entry = ttb.Spinbox(self.timer_entry_frame, from_=0, to=99, bootstyle=PRIMARY, width=5)
        self.minutes_entry = ttb.Spinbox(self.timer_entry_frame, from_=0, to=59, bootstyle=PRIMARY, width=5)
        self.seconds_entry = ttb.Spinbox(self.timer_entry_frame, from_=0, to=59, bootstyle=PRIMARY, width=5)

        self.hours_entry.grid(row=0, column=0, ipadx=0, ipady=0)
        self.divider.grid(row=0, column=1, padx=20)
        self.minutes_entry.grid(row=0, column=2)
        self.divider2.grid(row=0, column=3, padx=20)
        self.seconds_entry.grid(row=0, column=4)

        self.timer_entry_frame.grid(row=0, column=0, padx=50)

        self.start_timer_btn = ttb.Button(self.selector, text="START", bootstyle=(SUCCESS, OUTLINE),
                                          command=start_timer)
        self.start_timer_btn.grid(row=1, column=0, padx=50, pady=50)


def main():
    def change_frames(frame):
        timer_frame.grid_forget()
        time_frame.grid_forget()
        frame.grid(row=1, column=1)

    root = ttb.Window(themename="darkly")
    root.title("Clock")
    root.geometry("500x500")
    root.resizable(False, False)
    root.iconphoto(False, ImageTk.PhotoImage(file=resource_path("clock_icon.png")))

    side_panel = ttb.Frame(root, width=75, height=500, bootstyle="info")
    side_panel.grid(rowspan=4, column=0)

    clock_image = Image.open(resource_path("clock_icon.png"))
    resized_clock = clock_image.resize((50, 50))
    timer_image = Image.open(resource_path("timer_icon.png"))
    resized_timer = timer_image.resize((50, 50))

    used_clock_image = ImageTk.PhotoImage(resized_clock)
    used_timer_image = ImageTk.PhotoImage(resized_timer)

    clock_button = ttb.Button(root, image=used_clock_image, bootstyle=INFO, command=lambda: change_frames(time_frame))
    clock_button.image = used_clock_image
    clock_button.grid(row=0, column=0)

    timer_button = ttb.Button(root, image=used_timer_image, bootstyle=INFO, command=lambda: change_frames(timer_frame))
    timer_button.image = used_timer_image
    timer_button.grid(row=1, column=0)

    time_frame = TimeFrame(root).selector
    time_frame.grid(row=1, column=1)
    timer_frame = TimerFrame(root).selector

    root.mainloop()


if __name__ == '__main__':
    main()
