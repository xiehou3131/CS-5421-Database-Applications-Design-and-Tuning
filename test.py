import tkinter as tk

root = tk.Tk() # 创建一个窗口对象

# 创建一个标签
label = tk.Label(root, text="Hello World!", font=("Arial", 24))
label.pack() # 将标签添加到窗口

# 创建一个按钮
button = tk.Button(root, text="Click me!", command=lambda: print("Button clicked!"))
button.pack() # 将按钮添加到窗口

root.mainloop() # 进入主循环，等待用户交互