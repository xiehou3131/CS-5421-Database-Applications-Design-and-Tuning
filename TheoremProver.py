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
    global F
    global G

    text = input_box_schema.get()
    input_box_schema.delete(0, tk.END)

    words = [word.strip() for word in text.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        R = set(words)
        F = []
        G = []
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
                output_text.insert(tk.END, f"\nattribute '{word}' is not in the schema.")
                return
        
        LHS = words
    else:
        output_text.insert(tk.END, f"\nLHS '{text_LHS}' is not valid!")
        return

    words = []
    words = [word.strip() for word in text_RHS.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        for word in words:
            if word not in R:
                output_text.insert(tk.END, f"\nattribute '{word}' is not in the schema.")
                return
        
        RHS = words
    else:
        output_text.insert(tk.END, f"\nRHS '{text_RHS}' is not valid!")
        return

    FD = [LHS, RHS]
    F.append(FD)
    output_fds()

def on_button_click_goal():
    global R
    global F
    global G
    LHS = []
    RHS = []

    text_LHS = input_box_goal_LHS.get()
    text_RHS = input_box_goal_RHS.get()

    input_box_goal_LHS.delete(0, tk.END)
    input_box_goal_RHS.delete(0, tk.END)

    words = []
    words = [word.strip() for word in text_LHS.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        for word in words:
            if word not in R:
                output_text.insert(tk.END, f"\nattribute '{word}' is not in the schema.")
                return
        
        LHS = words
    else:
        output_text.insert(tk.END, f"\nLHS '{text_LHS}' is not valid!")
        return

    words = []
    words = [word.strip() for word in text_RHS.split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in words)
    if valid:
        for word in words:
            if word not in R:
                output_text.insert(tk.END, f"\nattribute '{word}' is not in the schema.")
                return
        
        RHS = words
    else:
        output_text.insert(tk.END, f"\nRHS '{text_RHS}' is not valid!")
        return

    G = [LHS, RHS]
    output_fds()

def output_fds():
    global R
    global F
    global G

    output_text.delete("1.0", tk.END)
    R_list = list(R)
    R_list.sort()
    output_text.insert(tk.END, f"schema = '{R_list}'")

    index = 0
    for fd in F:
        index += 1
        output_text.insert(tk.END, f"\n('{str(index)}') '{fd[0]}' -> '{fd[1]}'")

    if len(G) > 0:
        output_text.insert(tk.END, f"\nYour goal: '{G[0]}' -> '{G[1]}'")

R = {}
F = []
G = []

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

label_FD = tk.Label(left_frame, text="Please input the FDs")
label_FD.grid(row=4, column=0)
label_LHS = tk.Label(left_frame, text="Please input the LHS")
label_LHS.grid(row=5, column=0)
label_RHS = tk.Label(left_frame, text="Please input the RHS")
label_RHS.grid(row=5, column=1)
input_box_LHS = tk.Entry(left_frame)
input_box_LHS.grid(row=6, column=0)
input_box_RHS = tk.Entry(left_frame)
input_box_RHS.grid(row=6, column=1)
button_fd = tk.Button(left_frame, text="add", command=on_button_click_fd)
button_fd.grid(row=7, column=0)

label_goal = tk.Label(left_frame, text="Please input your goal")
label_goal.grid(row=9, column=0)
label_goal_LHS = tk.Label(left_frame, text="Please input the LHS")
label_goal_LHS.grid(row=10, column=0)
label_goal_RHS = tk.Label(left_frame, text="Please input the RHS")
label_goal_RHS.grid(row=10, column=1)
input_box_goal_LHS = tk.Entry(left_frame)
input_box_goal_LHS.grid(row=11, column=0)
input_box_goal_RHS = tk.Entry(left_frame)
input_box_goal_RHS.grid(row=11, column=1)
button_goal = tk.Button(left_frame, text="confirm", command=on_button_click_goal)
button_goal.grid(row=12, column=0)

# 右边的框架
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=2)

output_text = tk.Text(right_frame)
output_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 进入主循环，等待用户交互
root.mainloop()