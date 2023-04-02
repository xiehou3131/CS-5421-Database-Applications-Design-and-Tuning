# import tkinter as tk

# def on_button_click():
#     text = input_text.get().strip()
#     words = text.split(',')
#     valid_words = []
#     for word in words:
#         word = word.strip()
#         if len(word) == 1 and 'A' <= word <= 'Z':
#             valid_words.append(word)
#     output_text.delete("1.0", tk.END)
#     output_text.insert(tk.END, ", ".join(valid_words))

# root = tk.Tk()
# root.geometry("600x400")

# # 第一个输入框和按钮
# input_frame1 = tk.Frame(root)
# input_frame1.pack(side=tk.TOP, pady=20)

# label1 = tk.Label(input_frame1, text="Enter comma separated values:")
# label1.pack(side=tk.LEFT, padx=10)

# input_text = tk.Entry(input_frame1)
# input_text.pack(side=tk.LEFT)

# button = tk.Button(input_frame1, text="Submit", command=on_button_click)
# button.pack(side=tk.LEFT, padx=10)

# # 第二个和第三个输入框
# input_frame2 = tk.Frame(root)
# input_frame2.pack(side=tk.TOP, pady=20)

# label2 = tk.Label(input_frame2, text="Enter a single uppercase letter:")
# label2.pack(side=tk.LEFT, padx=10)

# input_text2 = tk.Entry(input_frame2)
# input_text2.pack(side=tk.LEFT)

# label3 = tk.Label(input_frame2, text="Enter another single uppercase letter:")
# label3.pack(side=tk.LEFT, padx=10)

# input_text3 = tk.Entry(input_frame2)
# input_text3.pack(side=tk.LEFT)

# # 输出框
# output_frame = tk.Frame(root)
# output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# output_label = tk.Label(output_frame, text="Valid letters:")
# output_label.pack(side=tk.TOP)

# output_text = tk.Text(output_frame, height=10)
# output_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# root.mainloop()

input_str = "A,B -> C"
input_arr = input_str.split("->")
print(input_arr)