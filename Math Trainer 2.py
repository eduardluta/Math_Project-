import tkinter as tk
import random
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Initialize score
score = 0

# Function to generate a random addition or multiplication question
def generate_question(mode, difficulty):
    if mode == 'addition':
        if difficulty == 'easy':
            num1, num2 = random.randint(0, 20), random.randint(0, 20)
        elif difficulty == 'medium':
            num1, num2 = random.randint(0, 100), random.randint(0, 100)
        else:  # hard
            num1, num2 = random.randint(0, 1000), random.randint(0, 1000)
        # Format the numbers to align properly using monospace font
        max_len = max(len(str(num1)), len(str(num2)))
        question = f"{num1:>{max_len}}\n+ {num2:>{max_len}}\n{'-' * (max_len)}"
        answer = num1 + num2
    elif mode == 'multiplication':
        if difficulty == 'easy':
            num1, num2 = random.randint(1, 5), random.randint(1, 5)
        elif difficulty == 'medium':
            num1, num2 = random.randint(1, 10), random.randint(1, 10)
        else:  # hard
            num1, num2 = random.randint(1, 20), random.randint(1, 20)
        question = f"{num1} × {num2} = ?"
        answer = num1 * num2
    else:
        question = ""
        answer = 0
    return question, answer

# Function to check the user's answer
def check_answer(event=None):
    global score
    user_answer = answer_entry.get()
    difficulty = difficulty_var.get()

    if user_answer.isdigit() and int(user_answer) == current_answer:
        if difficulty == 'easy':
            score += 1
        elif difficulty == 'medium':
            score += 2
        elif difficulty == 'hard':
            score += 3
        celebrate()
        answer_entry.unbind("<Return>")
        root.after(1000, new_question)  # Display new question after 1 second
    else:
        score -= 1  # Deduct 1 point for an incorrect answer
        messagebox.showerror("Incorrect", f"Oops! The correct answer is {current_answer}")
    
    score_label.config(text=f"Score: {score}")

# Function to display a new question
def new_question(event=None):
    global current_answer
    question, current_answer = generate_question(mode_var.get(), difficulty_var.get())
    question_label.config(text=question)
    answer_entry.delete(0, tk.END)
    next_button.pack_forget()
    celebration_label.config(text="", image="")
    answer_entry.bind("<Return>", check_answer)

# Function to set the mode and start the game
def set_mode(mode):
    mode_var.set(mode)
    new_question()

# Function to celebrate a correct answer
def celebrate():
    celebration_label.config(text="Correct! Great job! 🎉")
    if gif_image:
        celebration_label.config(image=gif_image)
        celebration_label.image = gif_image  # Keep reference to avoid garbage collection

# Function to proceed to the main game from the welcome screen
def start_game():
    welcome_label.pack_forget()
    start_button.pack_forget()
    difficulty_label.pack(pady=20)
    difficulty_frame.pack(pady=10)
    question_label.pack(pady=20)
    answer_entry.pack(pady=10)
    check_frame.pack(pady=20)  # Use a frame to hold check button and score
    button_frame.pack(pady=10)
    celebration_label.pack(pady=20)

# Set up the main window
root = tk.Tk()
root.title("Math Trainer for Kids")
root.geometry("1024x768")
root.minsize(600, 400)
root.configure(bg="#e6f7ff")  # Set a more vibrant and kid-friendly background color
for i in range(5):
    root.rowconfigure(i, weight=1)
    root.columnconfigure(i, weight=1)

# Set up UI elements for the welcome screen
welcome_label = tk.Label(root, text="Welcome to Math Trainer, Marin!", font=("Comic Sans MS", 36, "bold"), bg="#e6f7ff", fg="#3333cc")
welcome_label.pack(pady=80)

start_button = tk.Button(root, text="Start", command=start_game, font=("Comic Sans MS", 24, "bold"), bg="#33cc33", fg="white", relief="raised", borderwidth=5)
start_button.pack(pady=20)

# Set up UI elements for the main game
mode_var = tk.StringVar()
difficulty_var = tk.StringVar(value='easy')
question_label = tk.Label(root, text="Select Addition or Multiplication", font=("Courier", 32, "bold"), justify='left', anchor='w', bg="#e6f7ff", fg="#3333cc")

answer_entry = tk.Entry(root, font=("Comic Sans MS", 24), width=20, justify='center', relief="sunken", borderwidth=3)

# Frame for check button and score
check_frame = tk.Frame(root, bg="#e6f7ff")
check_button = tk.Button(check_frame, text="Check Answer", command=check_answer, font=("Comic Sans MS", 20, "bold"), bg="#33cc33", fg="white", relief="raised", borderwidth=3)
check_button.pack(side="left", padx=10)

score_label = tk.Label(check_frame, text=f"Score: {score}", font=("Comic Sans MS", 20, "bold"), bg="#e6f7ff", fg="#3333cc")
score_label.pack(side="left", padx=10)

next_button = tk.Button(root, text="Next Question", command=new_question, font=("Comic Sans MS", 20), bg="#3399ff", fg="white", relief="raised", borderwidth=3)
root.bind("<Right>", new_question)

# Frame for addition and multiplication buttons
button_frame = tk.Frame(root, bg="#e6f7ff")
addition_button = tk.Button(button_frame, text="Addition", command=lambda: set_mode('addition'), font=("Comic Sans MS", 24, "bold"), bg="#ff9933", fg="white", width=12, height=2, relief="raised", borderwidth=3)
multiplication_button = tk.Button(button_frame, text="Multiplication", command=lambda: set_mode('multiplication'), font=("Comic Sans MS", 24, "bold"), bg="#cc33ff", fg="white", width=12, height=2, relief="raised", borderwidth=3)
addition_button.pack(side="left", padx=10, pady=10)
multiplication_button.pack(side="left", padx=10, pady=10)

celebration_label = tk.Label(root, text="", font=("Comic Sans MS", 28, "bold"), fg="#33cc33", bg="#e6f7ff")

difficulty_label = tk.Label(root, text="Select Difficulty", font=("Comic Sans MS", 24, "bold"), bg="#e6f7ff", fg="#3333cc")
difficulty_frame = tk.Frame(root, bg="#e6f7ff")
easy_button = tk.Button(difficulty_frame, text="Easy", command=lambda: difficulty_var.set('easy'), font=("Comic Sans MS", 24, "bold"), bg="#33cc33", fg="white", width=12, height=2, relief="raised", borderwidth=3)
medium_button = tk.Button(difficulty_frame, text="Medium", command=lambda: difficulty_var.set('medium'), font=("Comic Sans MS", 24, "bold"), bg="#ffcc00", fg="white", width=12, height=2, relief="raised", borderwidth=3)
hard_button = tk.Button(difficulty_frame, text="Hard", command=lambda: difficulty_var.set('hard'), font=("Comic Sans MS", 24, "bold"), bg="#ff3333", fg="white", width=12, height=2, relief="raised", borderwidth=3)

# Arrange difficulty buttons horizontally
easy_button.pack(side="left", padx=10, pady=5)
medium_button.pack(side="left", padx=10, pady=5)
hard_button.pack(side="left", padx=10, pady=5)

# Load GIF image for celebration
if os.path.exists("celebration.gif"):
    gif_image = ImageTk.PhotoImage(Image.open("celebration.gif"))
else:
    gif_image = None

# Update font for question_label to monospace and align text
question_label.config(font=("Courier", 32, "bold"), justify='right')

# Run the main loop
root.mainloop()
