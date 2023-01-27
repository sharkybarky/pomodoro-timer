from tkinter import *
import pygame
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
COUNTDOWN_PERIOD_MS = 1 * 1000
# COUNTDOWN_PERIOD_MS = 1


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
class CountDownTimer:
    def __init__(self):
        self.countdown_from_in_secs = 0
        self.counting = False
        self.time_txt = None
        self.countdown_state_dict = {0: WORK_MIN, 1: SHORT_BREAK_MIN, 2: WORK_MIN, 3: SHORT_BREAK_MIN, 4: WORK_MIN,
                                     5: SHORT_BREAK_MIN, 6: WORK_MIN, 7: LONG_BREAK_MIN}
        self.state = None
        self.reset()

    def reset(self, state=0):
        if state == 0:
            self.counting = False
        self.state = state
        self.countdown_from_in_secs = self.countdown_state_dict[self.state] * 60
        self.update_text()
        print(f"State is now: {self.state}: {self.countdown_state_dict[self.state]} minutes")

    def start(self):
        self.counting = True

    def countdown(self, callback):
        if self.counting:
            if self.countdown_from_in_secs > 0:
                # count down the current state's time
                self.countdown_from_in_secs -= 1
                self.update_text()
                # print(self.time_txt)
            else:
                # move to the next state and adjust countdown_from_in_secs accordingly
                current_state = self.state
                current_state += 1
                # wrap around
                current_state = current_state % len(self.countdown_state_dict)
                self.reset(current_state)
                callback(self.time_txt, self.state)
                return

        callback(self.time_txt, self.state)

    def update_text(self):
        mins, secs = divmod(self.countdown_from_in_secs, 60)
        self.time_txt = '{:02d}:{:02d}'.format(mins, secs)


# ---------------------------- UI SETUP ------------------------------- #
class TimerUI:
    def __init__(self, countdown_fcn, reset_countdown_fcn, start_countdown_fcn):

        self.app_window = Tk()
        self.app_window.title("Pomodoro Timer")

        self.app_window.config(padx=10, pady=10, background=YELLOW)

        self.canvas = Canvas(self.app_window, width=300, height=224, background=YELLOW, highlightthickness=0)
        self.tomato = PhotoImage(file="tomato.png")
        self.canvas.create_image(150, 112, anchor=CENTER, image=self.tomato)
        self.countdown_wgt = self.canvas.create_text(150, 130, text="00:00", fill="white", font=(FONT_NAME, 20, "bold"))
        self.canvas.grid(row=1, column=1)

        self.timer_text_wgt = Label(text="Init", font=(FONT_NAME, 30, "bold"), foreground=GREEN, background=YELLOW)
        self.timer_text_wgt.grid(row=0, column=1)

        self.start_countdown_fcn = start_countdown_fcn
        self.start_button_wgt = Button()
        self.start_button_wgt.config(text="Start", command=self.start)
        self.start_button_wgt.grid(row=2, column=0)

        self.reset_countdown_fcn = reset_countdown_fcn
        self.reset_button_wgt = Button()
        self.reset_button_wgt.config(text="Reset", command=self.reset)
        self.reset_button_wgt.grid(row=2, column=2)

        self.tick_display_wgt = Label(text=" ", foreground=GREEN, background=YELLOW)
        self.num_ticks = 1
        self.display_ticks()

        self.prev_state = None

        self.countdown_fcn = countdown_fcn

    def start(self):
        self.start_countdown_fcn()

    def reset(self):
        self.reset_countdown_fcn()
        self.num_ticks = 1
        self.display_ticks()

    def display_ticks(self):
        tick_str = "".join(["✔" for _ in range(self.num_ticks)])
        self.tick_display_wgt.config(text=tick_str)
        self.tick_display_wgt.grid(row=3, column=1)

    def play_music(self, mp3):
        pygame.mixer.init()
        pygame.mixer.music.load(mp3)
        pygame.mixer.music.play(loops=0)

    def perpetual_timer(self, time_txt="00:00", state=0):
        self.app_window.after(COUNTDOWN_PERIOD_MS, self.countdown_fcn, self.perpetual_timer)
        self.canvas.itemconfig(self.countdown_wgt, text=time_txt)
        self.num_ticks = state + 1
        self.display_ticks()
        if state in (0, 2, 4, 6):
            self.timer_text_wgt.config(text="Work", foreground=GREEN)
            if self.prev_state and state != self.prev_state:
                self.play_music("hammer-sound5-37137.mp3")
        elif state == 7:
            self.timer_text_wgt.config(text="Long Rest", foreground=RED)
            if self.prev_state and state != self.prev_state:
                self.play_music("ocean-waves-112906.mp3")
        else:
            self.timer_text_wgt.config(text="Short Rest", foreground=PINK)
            if self.prev_state and state != self.prev_state:
                self.play_music("break-time-44678.mp3")

        self.prev_state = state

    def run(self):
        self.perpetual_timer()
        self.app_window.mainloop()


cdown = CountDownTimer()
ui = TimerUI(cdown.countdown, cdown.reset, cdown.start)
ui.run()
