import tkinter as tk
from prover import Prover

def on_button_click_schema():
    global R
    global F
    global G
    global PROVER
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
        PROVER = Prover(R)
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"input '{text}' is not valid!")

def on_button_click_fd():
    global R
    global PROVER
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
    proof_log = PROVER.we_know_that(FD)
    if proof_log:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"{PROVER.get_procedure()}")
    else:
        output_text.insert(tk.END, f"\nerror!")

def on_button_click_goal():
    global R
    global F
    global G
    global PROVER
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
    proof_log =  PROVER.set_goal(G)
    if proof_log:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"{PROVER.get_procedure()}")
    else:
        output_text.insert(tk.END, f"\nerror!")

def on_button_click_proof():
    global R
    global F

    text = input_box_proof.get()

    if text == "Q.E.D.":
        if PROVER.finished():
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"{PROVER.get_procedure()}")
        else:
            output_text.insert(tk.END, f"\nerror!")
        return

    input_box_proof.delete(0, tk.END)

    words = [word.strip() for word in text.split("|")]

    # goal
    goal = words[0]
    goal_split = [word.strip() for word in goal.split("->")]
    if len(goal_split) != 2:
        output_text.insert(tk.END, f"\ninvalid goal!")
        return
    
    LHS = []
    RHS = []

    # LHS of the goal
    attributes = []
    attributes = [word.strip() for word in goal_split[0].split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in attributes)
    if valid:
        for word in attributes:
            if word not in R:
                output_text.insert(tk.END, f"\nattribute '{word}' is not in the schema.")
                return
        
        LHS = attributes
    else:
        output_text.insert(tk.END, f"\nLHS '{goal_split[0]}' is not valid!")
        return

    # RHS of the goal
    attributes = []
    attributes = [word.strip() for word in goal_split[1].split(",")]
    valid = all(len(word) == 1 and word.isupper() for word in attributes)
    if valid:
        for word in attributes:
            if word not in R:
                output_text.insert(tk.END, f"\nattribute '{word}' is not in the schema.")
                return
        
        RHS = attributes
    else:
        output_text.insert(tk.END, f"\nRHS '{goal_split[1]}' is not valid!")
        return


    goal = [LHS, RHS]

    # rule
    rule = words[1]

    if rule == "TRA":
        if len(words) != 4:
            output_text.insert(tk.END, f"\ninvalid proof!")
        
        index1 = 0
        index1_str = words[2]
        try:
            index1 = int(index1_str)
        except ValueError:
            output_text.insert(tk.END, f"\ninvalid index1!")
            return

        index2 = 0
        index2_str = words[3]
        try:
            index2 = int(index2_str)
        except ValueError:
            output_text.insert(tk.END, f"\ninvalid index2!")
            return

        proof_log = PROVER.transitivity(goal, index1, index2)
        if proof_log:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"{PROVER.get_procedure()}")
        else:
            output_text.insert(tk.END, f"\nerror!")

    elif rule == "AUG":
        if len(words) != 4:
            output_text.insert(tk.END, f"\ninvalid proof!")

        index = 0
        index_str = words[2]
        try:
            index = int(index_str)
        except ValueError:
            output_text.insert(tk.END, f"\ninvalid index!")
            return

        attributes_list = words[3]
        attributes = [word.strip() for word in attributes_list.split(",")]
        valid = all(len(word) == 1 and word.isupper() for word in attributes)
        if valid:
            for word in attributes:
                if word not in R:
                    output_text.insert(tk.END, f"\nattribute '{word}' is not in the schema.")
                    return
        else:
            output_text.insert(tk.END, f"\n'{attributes}' is not valid!")
            return

        proof_log = PROVER.augmentation(goal, index, attributes)
        if proof_log:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"{PROVER.get_procedure()}")
        else:
            output_text.insert(tk.END, f"\nerror!")

    elif rule == "REF":
        if len(words) != 2:
            output_text.insert(tk.END, f"\ninvalid proof!")
    
        proof_log = PROVER.reflexivity(goal)
        if proof_log:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"{PROVER.get_procedure()}")
        else:
            output_text.insert(tk.END, f"\nerror!")
        
    else: 
        output_text.insert(tk.END, f"\nerror!")
        return



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

PROVER = None
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

label_goal = tk.Label(left_frame, text="Please input your goal")
label_goal.grid(row=3, column=0)
label_goal_LHS = tk.Label(left_frame, text="Please input the LHS")
label_goal_LHS.grid(row=4, column=0)
label_goal_RHS = tk.Label(left_frame, text="Please input the RHS")
label_goal_RHS.grid(row=4, column=1)
input_box_goal_LHS = tk.Entry(left_frame)
input_box_goal_LHS.grid(row=5, column=0)
input_box_goal_RHS = tk.Entry(left_frame)
input_box_goal_RHS.grid(row=5, column=1)
button_goal = tk.Button(left_frame, text="confirm", command=on_button_click_goal)
button_goal.grid(row=6, column=0)

label_FD = tk.Label(left_frame, text="Please input the FDs")
label_FD.grid(row=7, column=0)
label_LHS = tk.Label(left_frame, text="Please input the LHS")
label_LHS.grid(row=8, column=0)
label_RHS = tk.Label(left_frame, text="Please input the RHS")
label_RHS.grid(row=8, column=1)
input_box_LHS = tk.Entry(left_frame)
input_box_LHS.grid(row=9, column=0)
input_box_RHS = tk.Entry(left_frame)
input_box_RHS.grid(row=9, column=1)
button_fd = tk.Button(left_frame, text="add", command=on_button_click_fd)
button_fd.grid(row=10, column=0)

label_proof = tk.Label(left_frame, text="Your proof:")
label_proof.grid(row=13, column=0)
input_box_proof = tk.Entry(left_frame)
input_box_proof.grid(row=14, column=0)
button_proof = tk.Button(left_frame, text="check", command=on_button_click_proof)
button_proof.grid(row=15, column=0)


# 右边的框架
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=2)

output_text = tk.Text(right_frame)
output_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 进入主循环，等待用户交互
root.mainloop()