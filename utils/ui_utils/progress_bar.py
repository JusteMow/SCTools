import states.states as states
import sys

#======================= Progress Bar ==============----------->
def update_progress_bar(total, bar_length=50):
    """
    Displays a progress bar in the console.

    Args:
        current (int): The current progress value.
        total (int): The total value for completion.
        bar_length (int): The length of the progress bar.
    """
    current = states.progress_bar + 1 
    percent = current / total
    arrow = '#' * int(percent * bar_length)
    spaces = ' ' * (bar_length - len(arrow))

    # Écrire la barre de progression dans stdout
    print(f"Progress: [{arrow}{spaces}] {percent:.1%}", end="\r")

    states.progress_bar = current
    if current == total:
        print("\nDone\n")