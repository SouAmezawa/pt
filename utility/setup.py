import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os
import sys
import zipfile
import tempfile
import shutil
import subprocess

class Installer:
    def __init__(self, root):
        self.root = root
        root.title("安装程序")
        root.geometry("300x200")
        root.resizable(False, False)

        # 获取压缩包路径（支持 PyInstaller 打包）
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.zip_path = os.path.join(base_path, 'setup.zip')

        # 创建临时目录，用于存放界面资源
        self.temp_dir = tempfile.mkdtemp(prefix="installer_")

        # 从压缩包中提取图标和右侧图片到临时目录
        self.extract_resources()

        # 设置窗口图标
        icon_path = os.path.join(self.temp_dir, 'res', 'icon', 'utility', 'download.ico')
        try:
            icon_image = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon_image)
        except:
            #raise
            pass  # 若文件缺失则忽略

        # 字体
        self.font = ("Unifont", 10)

        # 右侧图片（64x192）
        gif_path = os.path.join(self.temp_dir, 'res', 'images', 'utility', 'download.gif')
        self.img = tk.PhotoImage(file=gif_path)
        self.img_label = tk.Label(root, image=self.img)
        self.img_label.place(x=300 - 64, y=0, width=64, height=192)

        # 左侧主区域
        left_frame = tk.Frame(root, width=236, height=200)
        left_frame.place(x=0, y=0)
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="元素周期表 安装程序", font=self.font).pack(pady=5)

        self.text = scrolledtext.ScrolledText(
            left_frame, font=self.font, height=8, width=30, wrap=tk.WORD
        )
        self.text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        self.text.insert(tk.END, "点击“安装”选择目标目录并开始解压。\n")
        self.text.config(state=tk.DISABLED)

        self.btn = tk.Button(left_frame, text="安装", font=self.font, command=self.install)
        self.btn.pack(pady=5)

        # 绑定窗口关闭事件，清理临时目录
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_shortcut(self, target_path, shortcut_name):
        """使用 PowerShell 在桌面创建快捷方式"""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
        ps_cmd = f'''
        $WScriptShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WScriptShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{target_path}"
        $Shortcut.Save()
        '''
        try:
            subprocess.run(
                ["powershell", "-Command", ps_cmd],
                check=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW  # 不显示窗口
            )
            self.text.insert(tk.END, f"桌面快捷方式已创建：{shortcut_path}\n")
            return True
        except Exception as e:
            self.text.insert(tk.END, f"创建快捷方式失败：{e}\n")
            return False

    def extract_resources(self):
        """从压缩包中提取界面所需的图标和图片到临时目录"""
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zf:
                # 需要提取的文件列表（保持目录结构）
                files_to_extract = [
                    'res/icon/utility/download.ico',
                    'res/images/utility/download.gif'
                ]
                for f in files_to_extract:
                    try:
                        zf.extract(f, self.temp_dir)
                    except KeyError:
                        pass  # 文件不存在则忽略
        except Exception as e:
            messagebox.showerror("错误", f"无法读取安装包资源：{e}")

    def install(self):
        """选择目标目录并解压所有文件"""
        target_dir = filedialog.askdirectory(title="选择安装目录")
        if not target_dir:
            return

        # 启用文本区并清空
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"正在解压到：{target_dir}\n")
        self.text.see(tk.END)
        self.root.update()

        # 禁用按钮，防止重复点击
        self.btn.config(state=tk.DISABLED)

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zf:
                total = len(zf.namelist())
                for i, name in enumerate(zf.namelist(), 1):
                    # 跳过临时已提取的资源文件（它们不在目标目录中）
                    # 但为了简洁，直接解压所有文件，覆盖目标目录中的同名文件
                    zf.extract(name, target_dir)
                    self.text.insert(tk.END, f"({i}/{total}) {name}\n")
                    self.text.see(tk.END)
                    self.root.update()

            # 解压完成后创建桌面快捷方式
            main_exe = "pt.exe"          # 请根据实际压缩包中的主程序文件名修改
            shortcut_name = "元素周期表"      # 请修改为您的软件名称
            target_exe = os.path.join(target_dir, main_exe)
            if os.path.exists(target_exe):
                self.create_shortcut(target_exe, shortcut_name)
            else:
                self.text.insert(tk.END, f"未找到主程序 {main_exe}，跳过创建快捷方式。\n")
            # 安装完成
            self.text.insert(tk.END, "\n安装完成！")
            self.text.see(tk.END)
            messagebox.showinfo("安装完成", "软件已成功安装到所选目录。")
        except Exception as e:
            self.text.insert(tk.END, f"\n安装失败：{e}")
            self.text.see(tk.END)
            messagebox.showerror("错误", f"安装过程中发生错误：{e}")
        finally:
            self.btn.config(state=tk.NORMAL)
            # 清理临时目录
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except:
                pass

    def on_closing(self):
        """关闭窗口时清理临时目录"""
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Installer(root)
    root.mainloop()
