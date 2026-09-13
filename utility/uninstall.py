import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import shutil
import sys
import subprocess

class Uninstaller:
    def __init__(self, root):
        self.root = root
        root.title("卸载程序")
        root.geometry("300x200")
        root.resizable(False, False)

        # 设置窗口图标
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        icon_path = os.path.join(base_dir, "res", "icon", "utility", "uninstall.ico")
        try:
            icon_image = tk.PhotoImage(file='./res/icon/utility/uninstall.ico')
            root.iconphoto(True, icon_image)
        except:
            #raise
            pass

        self.font = ("Unifont", 10)

        # 右侧图片
        gif_path = os.path.join(base_dir, "res", "images", "utility", "uninstall.gif")
        self.img = tk.PhotoImage(file=gif_path)
        self.img_label = tk.Label(root, image=self.img)
        self.img_label.place(x=300 - 64, y=0, width=64, height=192)

        # 左侧主区域
        left_frame = tk.Frame(root, width=236, height=200)
        left_frame.place(x=0, y=0)
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="元素周期表 卸载程序", font=self.font).pack(pady=5)

        self.text = scrolledtext.ScrolledText(
            left_frame, font=self.font, height=8, width=30, wrap=tk.WORD
        )
        self.text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        self.btn = tk.Button(left_frame, text="开始卸载", font=self.font, command=self.confirm_uninstall)
        self.btn.pack(pady=5)

        self.base_dir = base_dir
        self.self_path = os.path.abspath(sys.argv[0])

    def confirm_uninstall(self):
        """弹出确认对话框"""
        if messagebox.askyesno("确认卸载", "确定要卸载本程序及其所有文件吗？\n此操作不可撤销！"):
            self.uninstall()

    def uninstall(self):
        """执行卸载操作"""
        self.btn.config(state=tk.DISABLED)
        self.text.insert(tk.END, "正在准备卸载...\n")
        self.text.see(tk.END)
        self.root.update()

        # 释放图片资源
        self.img_label.destroy()
        self.img = None
        self.root.update()

        # 删除除自身外的所有文件和目录
        try:
            for item in os.listdir(self.base_dir):
                item_path = os.path.join(self.base_dir, item)
                if os.path.abspath(item_path) == self.self_path:
                    continue
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                    self.text.insert(tk.END, f"删除目录: {item_path}\n")
                else:
                    os.remove(item_path)
                    self.text.insert(tk.END, f"删除文件: {item_path}\n")
                self.text.see(tk.END)
                self.root.update()
        except Exception as e:
            self.text.insert(tk.END, f"卸载出错: {e}\n")
            self.btn.config(state=tk.NORMAL)
            return

        self.text.insert(tk.END, "所有文件已删除，正在卸载自身...\n")
        self.text.see(tk.END)
        self.root.update()

        # 启动后台命令删除自身和空目录
        cmd = (
            f'start /b cmd /c "cd %temp% && '
            f'del /f /q "{self.self_path}" && '
            f'rmdir /s /q "{self.base_dir}""'
        )
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 弹出卸载完成提示
        messagebox.showinfo("卸载完成", "程序及其所有文件已成功卸载。")
        
        # 退出程序
        self.root.quit()
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = Uninstaller(root)
    root.mainloop()
