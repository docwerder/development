import argparse
import time
import os

def show_notification(title, subtitle, message):
    # Play alert sound
    os.system('afplay /System/Library/Sounds/Glass.aiff')

    # Show notification
    os.system("""
              osascript -e 'display notification "{}" with title "{}" subtitle "{}" sound name "Glass"' 
              """.format(message, title, subtitle))


def start_pomodoro(pomodoro_time):
    """Startet einen Pomodoro Timer."""
    print("Starte Pomodoro...")
    time_left = pomodoro_time
    while time_left > 0:
        minutes, seconds = divmod(time_left, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        print(f"Zeit übrig: {time_str}")
        time.sleep(1)
        time_left -= 1
    print("Pomodoro beendet.")
    show_notification("Pomodoro abgeschlossen", "", "Zeit ist abgelaufen.")

def take_short_break(short_break_time):
    """Macht eine kurze Pause."""
    print("Mache kurze Pause...")
    time_left = short_break_time
    while time_left > 0:
        minutes, seconds = divmod(time_left, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        print(f"Zeit übrig: {time_str}")
        time.sleep(1)
        time_left -= 1
    show_notification("Kurze Pause beendet", "", "Zeit für den nächsten Pomodoro.")

def take_long_break(long_break_time):
    """Macht eine lange Pause."""
    print("Mache lange Pause...")
    time_left = long_break_time
    while time_left > 0:
        minutes, seconds = divmod(time_left, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        print(f"Zeit übrig: {time_str}")
        time.sleep(1)
        time_left -= 1
    show_notification("Lange Pause beendet", "", "Zeit für den nächsten Pomodoro.")

def main(pomodoro_time, short_break_time, long_break_time, num_pomodoros):
    """Hauptfunktion des Skripts."""
    pomodoros_completed = 0
    while True:
        start_pomodoro(pomodoro_time)
        pomodoros_completed += 1
        if pomodoros_completed == num_pomodoros:
            take_long_break(long_break_time)
            pomodoros_completed = 0
        else:
            take_short_break(short_break_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pomodoro-Technik Skript')
    parser.add_argument('pomodoro_time', type=int, help='Länge des Pomodoro in Sekunden')
    parser.add_argument('short_break_time', type=int, help='Länge der kurzen Pause in Sekunden')
    parser.add_argument('long_break_time', type=int, help='Länge der langen Pause in Sekunden')
    parser.add_argument('num_pomodoros', type=int, help='Anzahl von Pomodoros bis zur langen Pause')
    args = parser.parse_args()
    main(args.pomodoro_time, args.short_break_time, args.long_break_time, args.num_pomodoros)
