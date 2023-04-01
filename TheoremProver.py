import tkinter as tk

def get_closure(R, F, S):

    closure = set(S)

    while True:
    

        closure_backup = set(closure)

        # iterate the functional dependencies to check if there is a left hand side subset of the current closure
        for FD in F:
            if set(FD[0]).issubset(closure):
                closure.update(FD[1])

        # loop until there is no update to the closure
        if closure_backup == closure:
            break

    return list(closure)

def on_button_click_schema():
    global R

    text = input_box_schema.get()
    words = [word.strip() for word in text.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        R = set(words)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"input '{text}' is valid.")
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"input '{text}' is not valid!")

def on_button_click_fd():
    global R
    global F
    LHS = []
    RHS = []

    text_LHS = input_box_LHS.get()
    text_RHS = input_box_RHS.get()

    input_box_LHS.delete(0, tk.END)
    input_box_RHS.delete(0, tk.END)

    words = []
    words = [word.strip() for word in text_LHS.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        for word in words:
            if word not in R:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, f"attribute '{word}' is not in the schema.")
                return
        
        LHS = words
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"LHS '{text_LHS}' is not valid!")
        return

    words = []
    words = [word.strip() for word in text_RHS.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        for word in words:
            if word not in R:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, f"attribute '{word}' is not in the schema.")
                return
        
        RHS = words
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"RHS '{text_RHS}' is not valid!")
        return

    FD = [LHS, RHS]
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"functional dependency '{LHS}' -> '{RHS}' added")
    F.append(FD)

def on_button_click_attributes():
    global R
    global F
    global S
    
    text = input_box_attributes.get()
    words = [word.strip() for word in text.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        for word in words:
            if word not in R:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, f"attribute '{word}' is not in the schema.")
                return
        
        S = set(words)

        closure = get_closure(R, F, S)

        print(closure)
        
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"the closure is '{closure}'.")
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"input '{text}' is not valid!")

R = {}
F = []
S = {}

# 创建主窗口
root = tk.Tk()
root.title("Theorem prover")

# 左边的框架
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0)

# 创建标签、输入框和确定按钮
label_schema = tk.Label(left_frame, text="Please input the schema")
label_schema.grid(row=0, column=0)
input_box_schema = tk.Entry(left_frame)
input_box_schema.grid(row=1, column=0)
button_schema = tk.Button(left_frame, text="confirm", command=on_button_click_schema)
button_schema.grid(row=2, column=0)

label_LHS = tk.Label(left_frame, text="Please input the LHS")
label_LHS.grid(row=3, column=0)
label_RHS = tk.Label(left_frame, text="Please input the RHS")
label_RHS.grid(row=3, column=1)
input_box_LHS = tk.Entry(left_frame)
input_box_LHS.grid(row=4, column=0)
input_box_RHS = tk.Entry(left_frame)
input_box_RHS.grid(row=4, column=1)
button_fd = tk.Button(left_frame, text="confirm", command=on_button_click_fd)
button_fd.grid(row=5, column=0)

label_attributes = tk.Label(left_frame, text="Please input the attributes")
label_attributes.grid(row=6, column=0)
input_box_attributes = tk.Entry(left_frame)
input_box_attributes.grid(row=7, column=0)
button_attributes = tk.Button(left_frame, text="confirm", command=on_button_click_attributes)
button_attributes.grid(row=8, column=0)

# 右边的框架
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=2)

output_text = tk.Text(right_frame)
output_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 进入主循环，等待用户交互
root.mainloop()