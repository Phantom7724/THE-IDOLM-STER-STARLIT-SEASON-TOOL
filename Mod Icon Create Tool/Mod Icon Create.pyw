import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw

# 设置文件路径
SETTINGS_FILE = "settings.json"

# 读取设置文件，如果不存在返回默认值
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"input_folder": "", "output_folder": ""}

# 保存设置到文件
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def select_input_folder():
    folder_selected = filedialog.askdirectory(title="选择输入文件夹")
    if folder_selected:
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(0, folder_selected)
        settings['input_folder'] = folder_selected
        save_settings(settings)

def select_output_folder():
    folder_selected = filedialog.askdirectory(title="选择输出文件夹")
    if folder_selected:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_selected)
        settings['output_folder'] = folder_selected
        save_settings(settings)

def process_images(input_folder, output_folder):
    try:
        # 检查输入文件夹是否存在
        if not os.path.exists(input_folder):
            messagebox.showerror("错误", "输入文件夹不存在")
            return

        # 检查输出文件夹是否存在，不存在则创建
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 定义选区在 2560x1440 分辨率下的位置
        base_resolution = (2560, 1440)
        base_selection = {
            "top": 301,
            "left": 1570,
            "bottom": 848,
            "right": 2117
        }

        # 遍历输入文件夹内的所有图像
        for filename in os.listdir(input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                filepath = os.path.join(input_folder, filename)
                img = Image.open(filepath).convert("RGBA")
                img_width, img_height = img.size

                # 计算选区在当前图像中的位置
                scale_x = img_width / base_resolution[0]
                scale_y = img_height / base_resolution[1]

                selection = {
                    "top": int(base_selection["top"] * scale_y),
                    "left": int(base_selection["left"] * scale_x),
                    "bottom": int(base_selection["bottom"] * scale_y),
                    "right": int(base_selection["right"] * scale_x)
                }

                cropped_img = img.crop((selection["left"], selection["top"], selection["right"], selection["bottom"]))

                # 转换图像大小，使用 LANCZOS 替代 ANTIALIAS
                cropped_img = cropped_img.resize((235, int(cropped_img.height * 235 / cropped_img.width)), Image.Resampling.LANCZOS)

                # 调整画布大小并居中
                canvas_img = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
                offset = ((256 - cropped_img.width) // 2, (256 - cropped_img.height) // 2)
                canvas_img.paste(cropped_img, offset, cropped_img)

                # 置入外部图片 (Default Icon.png)
                icon_path = os.path.join(os.getcwd(), "Default Icon.png")
                if os.path.exists(icon_path):
                    icon_img = Image.open(icon_path).convert("RGBA")
                    icon_offset = ((256 - icon_img.width) // 2, (256 - icon_img.height) // 2)
                    canvas_img.paste(icon_img, icon_offset, icon_img)

                # 保存为 TGA 格式
                output_filepath = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.tga")
                canvas_img.save(output_filepath, format="TGA", bits=32)

                print(f"处理完成: {filename} 保存到 {output_filepath}")

        messagebox.showinfo("完成", "All images processed")
    except Exception as e:
        messagebox.showerror("错误", f"处理过程中发生错误: {e}")

def start_processing():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()

    if not input_folder or not output_folder:
        messagebox.showwarning("警告", "Please select input and output folders")
        return

    process_images(input_folder, output_folder)

def on_closing():
    # 保存设置到文件
    settings['input_folder'] = input_folder_entry.get()
    settings['output_folder'] = output_folder_entry.get()
    save_settings(settings)
    root.destroy()

# 读取设置文件
settings = load_settings()

# 创建 UI 界面
root = tk.Tk()
root.title("THE IDOLM STER STARLIT SEASON MOD ICON CREATE TOOL")

tk.Label(root, text="Input Folder:").grid(row=0, column=0, padx=10, pady=5)
input_folder_entry = tk.Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=5)

tk.Button(root, text="Start", command=start_processing).grid(row=2, column=1, padx=10, pady=20)

# 加载上次使用的输入和输出文件夹
input_folder_entry.insert(0, settings.get("input_folder", ""))
output_folder_entry.insert(0, settings.get("output_folder", ""))

# 注册退出事件处理函数
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
