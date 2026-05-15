import tkinter as tk
from tkinter import ttk
import os
import re
import sys

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "markdown")


def sanitize_filename(title):
    """Extract a safe filename from the title text."""
    name = title.strip()
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = name.replace(' ', '_')
    return name if name else "untitled"


def generate_md(prob_text, sol_text, status_label):
    """Generate the markdown file from problem and solution text."""
    if not prob_text.strip():
        status_label.config(text="错误：题目内容不能为空", foreground="red")
        return

    lines = prob_text.split('\n')
    first_line = lines[0].rstrip()
    rest_lines = '\n'.join(lines[1:]) if len(lines) > 1 else ''

    # Process heading: ensure it's a level-1 heading
    heading_match = re.match(r'^(#{1,6})\s+(.*)', first_line)
    if heading_match:
        heading_text = heading_match.group(2)
    else:
        heading_text = first_line

    # Build the title: # [每日算法] + original heading text
    title_line = f'# [每日算法]{heading_text}'

    # Build the content
    parts = [title_line]
    if rest_lines.strip():
        parts.append(rest_lines.strip())
    parts.append('---')
    parts.append('# 题解')
    parts.append('```cpp')
    parts.append(sol_text.strip() if sol_text.strip() else '')
    parts.append('```')

    content = '\n\n'.join(parts) + '\n'

    # Determine filename and save
    filename = sanitize_filename(heading_text) + '.md'
    filepath = os.path.join(OUTPUT_DIR, filename)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    status_label.config(
        text=f"已生成：{filepath}", foreground="green")


def open_algorithm_window(root):
    """Open the '每日算法' input window."""
    win = tk.Toplevel(root)
    win.title("每日算法")
    win.geometry("700x650")
    win.minsize(500, 400)

    # --- Bottom bar: packed first so it's always visible ---
    bottom_frame = ttk.Frame(win)
    bottom_frame.pack(side="bottom", fill="x", padx=12, pady=(4, 10))

    status_label = ttk.Label(bottom_frame, text="", foreground="gray")
    status_label.pack(side="left", fill="x", expand=True)

    def on_generate():
        generate_md(
            prob_text.get("1.0", "end-1c"),
            sol_text.get("1.0", "end-1c"),
            status_label,
        )

    ttk.Button(bottom_frame, text="生成", command=on_generate).pack(side="right")

    # --- Problem input ---
    ttk.Label(win, text="题目（Markdown 格式）", font=("", 10, "bold")).pack(
        anchor="w", padx=12, pady=(12, 2))
    prob_frame = ttk.Frame(win)
    prob_frame.pack(fill="both", expand=True, padx=12, pady=(0, 4))
    prob_text = tk.Text(prob_frame, wrap="word", font=("Consolas", 10))
    prob_scroll = ttk.Scrollbar(prob_frame, command=prob_text.yview)
    prob_text.configure(yscrollcommand=prob_scroll.set)
    prob_scroll.pack(side="right", fill="y")
    prob_text.pack(side="left", fill="both", expand=True)

    # --- Solution input ---
    ttk.Label(win, text="题解（C++ 代码）", font=("", 10, "bold")).pack(
        anchor="w", padx=12, pady=(4, 2))
    sol_frame = ttk.Frame(win)
    sol_frame.pack(fill="both", expand=True, padx=12, pady=(0, 6))
    sol_text = tk.Text(sol_frame, wrap="none", font=("Consolas", 10))
    sol_scroll_y = ttk.Scrollbar(sol_frame, orient="vertical",
                                 command=sol_text.yview)
    sol_scroll_x = ttk.Scrollbar(sol_frame, orient="horizontal",
                                 command=sol_text.xview)
    sol_text.configure(yscrollcommand=sol_scroll_y.set,
                       xscrollcommand=sol_scroll_x.set)
    sol_scroll_y.pack(side="right", fill="y")
    sol_scroll_x.pack(side="bottom", fill="x")
    sol_text.pack(side="left", fill="both", expand=True)


def main():
    root = tk.Tk()
    root.title("博客工具")
    root.geometry("320x180")
    root.resizable(False, False)

    ttk.Label(root, text="博客 Markdown 生成工具",
              font=("", 12, "bold")).pack(pady=(30, 20))
    ttk.Button(root, text="每日算法",
               command=lambda: open_algorithm_window(root)).pack(pady=10)
    ttk.Label(root, text="选择功能按钮以开始", foreground="gray").pack(pady=(10, 0))

    root.mainloop()


if __name__ == '__main__':
    main()
