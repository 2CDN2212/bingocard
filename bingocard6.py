import tkinter as tk
import random

CARD_SIZE = 5

NUMBERS_RANGE = list(range(1, 76))

def create_bingo_card(): 
    card = []
    for i in range(CARD_SIZE):
        column_numbers = random.sample(NUMBERS_RANGE[i * 15 :(i + 1) * 15], CARD_SIZE)
        card.append(column_numbers)
    card[CARD_SIZE//2][CARD_SIZE//2] = "Free" 
    return card

def transpose_card(card):
    return [list(row) for row in zip(*card)]

def button_click(button, i, j, selected, status_label):
    button.config(bg="lightgreen")
    selected[i][j] = True
    check_bingo(selected, status_label)

def check_bingo(selected, status_label):
    rows = [all(row) for row in selected]
    cols = [all(col) for col in zip(*selected)]
    diag1 = all(selected[i][i] for i in range(CARD_SIZE))
    diag2 = all(selected[i][CARD_SIZE - i - 1] for i in range(CARD_SIZE))

    if any(rows) or any(cols) or diag1 or diag2:
        status_label.config(text = "ビンゴ！")
    elif any(sum(row) == CARD_SIZE - 1 for row in selected) or \
         any(sum(col) == CARD_SIZE - 1 for col in zip(*selected)) or \
         sum(selected[i][i] for i in range(CARD_SIZE)) == CARD_SIZE - 1 or \
         sum(selected[i][CARD_SIZE - i - 1] for i in range(CARD_SIZE)) == CARD_SIZE - 1:
        status_label.config(text = "リーチ！")
    else:
        status_label.config(text="")

def reset_card(root, status_label):
    for widget in root.winfo_children():
        widget.destroy()
    new_card = create_bingo_card()
    transposed_card = transpose_card(new_card)

    status_label = tk.Label(root, text="", font=("Helvetica", 16))
    display_bingo_card(root, transposed_card, status_label)

def display_bingo_card(root, card, status_label):
    selected = [[False] * CARD_SIZE for _ in range(CARD_SIZE)]
    for i in range(CARD_SIZE):
        for j in range(CARD_SIZE):
            text = str(card[i][j])
            if text == "Free":
                button = tk.Button(root, text=text, font=("Helvetica", 20), width=5, height=2, state="disabled", bg="lightgray")
                selected[i][j] = True 
            else:
                button = tk.Button(root, text=text, font=("Helvetica", 20), width=5, height=2)
                button.config(command=lambda b=button, x=i, y=j: button_click(b, x, y, selected, status_label))
            button.grid(row=i, column=j)

    reset_button = tk.Button(root, text="リセット", font=("Helvetica", 16), command=lambda: reset_card(root, status_label))
    reset_button.grid(row=CARD_SIZE, column=0, columnspan=CARD_SIZE, pady=10)

   
    status_label.grid(row=CARD_SIZE + 1, column=0, columnspan=CARD_SIZE)

    reset_button = tk.Button(root, text="リセット", font=("Helvetica", 16), command=lambda: reset_card(root, status_label))
    reset_button.grid(row=CARD_SIZE, column=0, columnspan=CARD_SIZE, pady=10)

    status_label.grid(row=CARD_SIZE + 1, column=0, columnspan=CARD_SIZE)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ビンゴカード")
    

    status_label = tk.Label(root, text="", font=("Helvetica", 16))
    

    bingo_card = create_bingo_card()
    transposed_card = transpose_card(bingo_card)
    display_bingo_card(root, transposed_card, status_label)
    
    root.mainloop()
