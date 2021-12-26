from tkinter import Button, Tk, Label, X
import winsound
import datetime
import sys
import time
from AlGUILoop.AlGUILoop import AlGUILoop


def AlAlarm(alarmTime):

    @AlGUILoop
    def setAlarm(alarmTime):
        alarmTime = alarmTime.split(':')
        hourAlarm = int(alarmTime[0])
        minuteAlarm = int(alarmTime[1])
        while True:
            if hourAlarm == datetime.datetime.now().hour:
                if minuteAlarm == datetime.datetime.now().minute:
                    winsound.PlaySound('Alarm.wav', winsound.SND_LOOP)
                    yield 0.2
                elif minuteAlarm < datetime.datetime.now().minute:
                    break
        exit()

    root = Tk()
    root.geometry("360x200+1460+815")
    root.configure(background='black')
    root.resizable(0, 0)
    root.overrideredirect(1)
    root.lift()
    root.attributes('-topmost', True)

    def liftWindow():
        root.lift()
        root.after(1000, liftWindow)

    def start():
        textTime = time.strftime('%H:%M:%S')
        label.config(text=textTime)
        label.after(200, start)

    def stop():
        exit()

    label = Label(root, font=('ds-digital', 50, 'bold'), bg='black', fg='red',
                  bd=50)
    label.pack(fill=X)

    stop = Button(root, font=('Segoe UI', 15, 'bold'), bg='white', fg='black',
                  text="STOP", command=stop, borderwidth=0,
                  highlightthickness=3)
    stop.pack(fill=X)

    start()
    setAlarm(root, alarmTime)
    liftWindow()
    root.mainloop()


if __name__ == "__main__":
    AlAlarm(sys.argv[1])
