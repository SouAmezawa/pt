import tkinter as tk
from tkinter import scrolledtext
import os
import sys
import webbrowser

class Updater:
    def __init__(self, root):
        self.root = root
        root.title("更新程序")
        root.geometry("300x200")
        root.resizable(False, False)

        # 设置窗口图标
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        icon_path = os.path.join(base_dir, "res", "icon", "utility", "update.ico")
        try:
            icon_image = tk.PhotoImage(file='./res/icon/utility/update.ico')
            root.iconphoto(True, icon_image)
        except:
            #raise
            pass  # 图标不存在时忽略

        # 字体
        self.font = ("Unifont", 10)

        # 右侧图片（64x192）
        gif_path = os.path.join(base_dir, "res", "images", "utility", "update.gif")
        self.img = tk.PhotoImage(file=gif_path)
        self.img_label = tk.Label(root, image=self.img)
        self.img_label.place(x=300 - 64, y=0, width=64, height=192)

        # 左侧主区域（宽度236，高度200）
        left_frame = tk.Frame(root, width=236, height=200)
        left_frame.place(x=0, y=0)
        left_frame.pack_propagate(False)

        # 标题
        tk.Label(left_frame, text="元素周期表 更新程序", font=self.font).pack(pady=5)

        # 滚动文本框（风格保留，用于显示提示信息）
        self.text = scrolledtext.ScrolledText(
            left_frame, font=self.font, height=8, width=30, wrap=tk.WORD
        )
        self.text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        self.text.insert(tk.END, "点击下方“更新”按钮将打开官网下载最新版本。\n")
        self.text.config(state=tk.DISABLED)  # 禁止编辑

        # 更新按钮
        self.btn = tk.Button(left_frame, text="更新", font=self.font, command=self.open_website)
        self.btn.pack(pady=5)

        # 官网地址（请替换为实际网址）
        self.url = "sivenioo-stu.ysepan.com"

    def open_website(self):
        """在默认浏览器中打开官网"""
        webbrowser.open(self.url)


if __name__ == "__main__":
    root = tk.Tk()
    app = Updater(root)
    root.mainloop()
