import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import logging

# 设置日志输出
log_file = "operation.log"
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 正则表达式提取 chr_body_cos***
pattern = re.compile(r"(chr_body_cos\d{3})")

# 选择目录的全局变量
selected_directory = ""

# 处理文件夹结构
def restructure_folders(directory):
    logging.info(f"开始处理目录：{directory}")

    # 标记是否有任何文件夹被处理
    any_folder_processed = False

    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        
        if os.path.isdir(folder_path):
            # 处理情况 1：文件夹包含 Mesh，Material，Texture
            if any(subfolder in os.listdir(folder_path) for subfolder in ["Mesh", "Material", "Texture"]):
                process_mesh_material_texture(folder_path)
                any_folder_processed = True
            # 处理情况 2：文件夹直接包含 chr_body_cos*** 文件夹
            elif any(re.match(pattern, subfolder) for subfolder in os.listdir(folder_path)):
                process_chr_body_cos_directly(folder_path)
                any_folder_processed = True
            # 处理情况 3：包含 Model 文件夹的子文件夹
            elif "Model" in os.listdir(folder_path):
                process_model_folder(folder_path)
                any_folder_processed = True
            # 处理情况 4：包含 Body 文件夹的子文件夹
            elif "Body" in os.listdir(folder_path):
                process_body_folder(folder_path)
                any_folder_processed = True

    if any_folder_processed:
        messagebox.showinfo("完成", "文件夹重构已完成！")
        logging.info("文件夹重构已完成")
    else:
        messagebox.showinfo("完成", "没有找到需要重构的文件夹。")
        logging.info("没有找到需要重构的文件夹。")

# 处理包含 Mesh, Material, Texture 的文件夹
def process_mesh_material_texture(folder_path):
    found_name = None
    for subfolder in ["Mesh", "Material", "Texture"]:
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.exists(subfolder_path):
            for file in os.listdir(subfolder_path):
                match = pattern.search(file)
                if match:
                    found_name = match.group(1)
                    logging.info(f"从文件 {file} 中提取到名称：{found_name}")
                    break
        if found_name:
            break
    
    if found_name:
        new_base_path = os.path.join(folder_path, "StarlitSeason", "Content", "Model", "Character", "Body", "Cos", found_name)
        # 确保目标路径存在
        if not os.path.exists(new_base_path):
            os.makedirs(new_base_path)
            logging.info(f"创建目录：{new_base_path}")

        # 移动 Mesh, Material, Texture 文件夹
        for subfolder in ["Mesh", "Material", "Texture"]:
            subfolder_path = os.path.join(folder_path, subfolder)
            if os.path.exists(subfolder_path):
                new_subfolder_path = os.path.join(new_base_path, subfolder)
                # 移动文件夹时检查是否已存在相同目录，避免套娃
                if not os.path.exists(new_subfolder_path):
                    shutil.move(subfolder_path, new_subfolder_path)
                    logging.info(f"移动文件夹：{subfolder_path} -> {new_subfolder_path}")

            # 删除空文件夹
            if os.path.exists(subfolder_path) and not os.listdir(subfolder_path):
                os.rmdir(subfolder_path)
                logging.info(f"删除空文件夹：{subfolder_path}")
    else:
        logging.warning(f"未找到有效的 chr_body_cos 名称，跳过文件夹：{folder_path}")

# 处理直接包含 chr_body_cos*** 的文件夹
def process_chr_body_cos_directly(folder_path):
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path) and re.match(pattern, subfolder):
            new_path = os.path.join(folder_path, "StarlitSeason", "Content", "Model", "Character", "Body", "Cos", subfolder)

            # 如果目标路径不存在，创建新目录
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                logging.info(f"创建目录：{new_path}")

            # 移动文件
            for item in os.listdir(subfolder_path):
                item_path = os.path.join(subfolder_path, item)
                new_item_path = os.path.join(new_path, item)

                if os.path.isdir(item_path) or os.path.isfile(item_path):
                    shutil.move(item_path, new_item_path)
                    logging.info(f"移动文件：{item_path} -> {new_item_path}")
            
            # 删除空文件夹
            if os.path.exists(subfolder_path) and not os.listdir(subfolder_path):
                os.rmdir(subfolder_path)
                logging.info(f"删除空文件夹：{subfolder_path}")

# 处理包含 Model 文件夹的情况
def process_model_folder(folder_path):
    new_path = os.path.join(folder_path, "StarlitSeason", "Content")
    
    # 创建新的 StarlitSeason/Content 目录
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        logging.info(f"创建目录：{new_path}")
    
    # 移动所有子文件夹到 StarlitSeason/Content 下
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path) and subfolder != "StarlitSeason":
            new_subfolder_path = os.path.join(new_path, subfolder)
            shutil.move(subfolder_path, new_subfolder_path)
            logging.info(f"移动文件夹：{subfolder_path} -> {new_subfolder_path}")

# 处理包含 Body 文件夹的情况
def process_body_folder(folder_path):
    new_path = os.path.join(folder_path, "StarlitSeason", "Content", "Model", "Character")

    # 创建新的 StarlitSeason/Content/Model/Character 目录
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        logging.info(f"创建目录：{new_path}")

    # 移动所有子文件夹到 StarlitSeason/Content/Model/Character 下
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path) and subfolder != "StarlitSeason":
            new_subfolder_path = os.path.join(new_path, subfolder)
            shutil.move(subfolder_path, new_subfolder_path)
            logging.info(f"移动文件夹：{subfolder_path} -> {new_subfolder_path}")

# 选择目录
def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory(title="选择处理目录")
    if selected_directory:
        directory_label.config(text=f"选择的目录：{selected_directory}")
        logging.info(f"选择的目录：{selected_directory}")
    else:
        directory_label.config(text="没有选择目录")

# 创建UI
def create_ui():
    window = tk.Tk()
    window.title("文件夹重构工具")

    # 选择目录按钮
    select_button = tk.Button(window, text="选择处理目录", command=select_directory)
    select_button.grid(column=0, row=0, padx=10, pady=10)

    global directory_label
    directory_label = tk.Label(window, text="选择的目录：")
    directory_label.grid(column=0, row=1, padx=10, pady=10)

    # 滚动文本框显示日志
    log_area = scrolledtext.ScrolledText(window, width=50, height=20, state='disabled')
    log_area.grid(column=0, row=2, padx=10, pady=10)
    
    # 开始按钮
    start_button = tk.Button(window, text="开始重构", command=lambda: restructure_folders(selected_directory))
    start_button.grid(column=0, row=3, padx=10, pady=10)

    # 显示日志按钮
    def show_logs():
        with open(log_file, 'r') as f:
            log_content = f.read()
            log_area.config(state='normal')
            log_area.delete(1.0, tk.END)
            log_area.insert(tk.INSERT, log_content)
            log_area.config(state='disabled')

    show_log_button = tk.Button(window, text="显示日志", command=show_logs)
    show_log_button.grid(column=0, row=4, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_ui()
