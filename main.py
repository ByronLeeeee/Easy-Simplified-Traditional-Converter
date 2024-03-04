import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import opencc
import pyperclip


class TextConverterApp:
    def __init__(self, master: ttk.Window, icon):
        self.master = master
        master.iconphoto(True, icon)
        master.resizable(False, False)  # 禁止窗口改变大小
        self.input_label = ttk.LabelFrame(master, text="输入文本")
        self.input_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.output_label = ttk.LabelFrame(master, text="输出文本")
        self.output_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.input_text = ttk.Text(self.input_label, height=5, width=50)
        self.input_text.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

        self.output_text = ttk.Text(self.output_label, height=5, width=50)
        self.output_text.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

        self.conversion_options = [
            "",
            "简体 → 繁体",
            "简体 → 繁体 (香港用词)",
            "简体 → 繁体 (台湾正体 + 用词)",
            "繁体 → 简体",
            "繁体 (台湾正体) → 简体",
            "繁体 (香港用词) → 简体",
            "繁体 (台湾正体) → 简体 (大陆用词)"
        ]

        self.selected_option = ttk.StringVar()
        self.selected_option.set(self.conversion_options[1])  # 默认选择第一个选项

        self.option_menu = ttk.OptionMenu(
            master, self.selected_option, *self.conversion_options)
        self.option_menu.grid(row=2, column=0, padx=10,
                              pady=5, columnspan=1, sticky=tk.E+tk.W)

        self.convert_button = ttk.Button(
            master, text="复制到剪贴板", command=self.copy_to_clipboard)
        self.convert_button.grid(
            row=3, column=0, columnspan=1, padx=10, pady=5, sticky=tk.N)

        self.about_button = ttk.Button(
            master, text="关于", command=self.show_about_info, bootstyle="secondary-link")
        self.about_button.grid(
            row=3, column=0, columnspan=1, padx=10, pady=5, sticky=tk.E)

        self.input_text.bind("<KeyRelease>", lambda event: self.convert_text())
        self.selected_option.trace_add('write', self.convert_text)

    def convert_text(self, *args):
        event = args[0] if args else None
        converter = self.get_converter()
        input_text = self.input_text.get("1.0", tk.END).strip()
        converted_text = converter.convert(input_text)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, converted_text)

    def copy_to_clipboard(self):
        converted_text = self.output_text.get("1.0", tk.END).strip()
        pyperclip.copy(converted_text)
        self.show_copied_message()

    def get_converter(self):
        conversion_option = self.selected_option.get()

        if "简体 → 繁体" in conversion_option:
            converter_type = 's2t.json'
        if "繁体 → 简体" in conversion_option:
            converter_type = 't2s.json'
        if "繁体 (台湾正体) → 简体" in conversion_option:
            converter_type = 'tw2s.json'
        if "简体 → 繁体 (香港用词)" in conversion_option:
            converter_type = 's2hk.json'
        if "繁体 (香港用词) → 简体" in conversion_option:
            converter_type = 'hk2s.json'
        if "简体 → 繁体 (台湾正体 + 用词)" in conversion_option:
            converter_type = 's2twp.json'
        if "繁体 (台湾正体) → 简体 (大陆用词)" in conversion_option:
            converter_type = 'tw2sp.json'

        return opencc.OpenCC(converter_type)

    def show_copied_message(self):
        copied_label = ttk.Label(self.master, text="已复制到粘贴板", style="success")
        copied_label.grid(row=3, column=0, columnspan=1,
                          padx=10, pady=5, sticky=tk.W)

    def show_about_info(self):
        Messagebox.ok(message="基于OpenCC的简易简繁转换器 Ver 1.0\n\n版权所有 © 2024 李伯阳-北京市隆安（广州）律师事务所\n\n联系方式(Wechat):legal-lby",title='关于')


def main():
    root = ttk.Window(themename='superhero', title="简繁转换器")
    root.position_center()
    # base64编码的图像数据
    base64_icon = """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"""
    icon = tk.PhotoImage(data=base64_icon)
    app = TextConverterApp(root, icon)
    root.mainloop()


if __name__ == "__main__":
    main()
