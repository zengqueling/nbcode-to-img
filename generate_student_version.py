import os
import re
import unicodedata

import matplotlib.pyplot as plt
import nbformat
from bs4 import BeautifulSoup
from matplotlib import font_manager
from nbformat.v4 import new_code_cell, new_markdown_cell
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

# 设置字体为YaHei Consolas Hybrid
plt.rcParams["font.family"] = "YaHei Consolas Hybrid"
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

# 浅色背景
code_background_color = "#f5f5f5"  # Light background color
text_color = "#333333"  # Dark text color
line_number_color = "#888888"  # Line number color
comment_color = "#5F9EA0"  # Blue color for comments
keyword_color = "#4169E1"  # Deep green color for import, from, as
operator_color = "#8B008B"  # Purple color for =
string_color = "#8B0000"  # Deep red color for strings
number_color = "#FF8C00"  # Dark orange color for numbers
operatorlist = ["=", "+", "-", "*", ":", "(", ")", "[", "]", "."]
keywordlist = [
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "print",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
]

# 高亮代码样式
formatter = HtmlFormatter(style="default", full=True, noclasses=True)


# 判断字符是否为全角字符
def is_full_width(char):
    return unicodedata.east_asian_width(char) in ("F", "W")


# 获取字符的宽度
def get_char_width(char):
    return 0.02 if is_full_width(char) else 0.009


# 判断字符串是否包含中文
def contains_chinese(text):
    return any("\u4e00" <= char <= "\u9fff" for char in text)


# 计算调整后的空白距离
def calculate_adjusted_spacing(text):
    chinese_count = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    english_count = len(text) - chinese_count
    chinese_reduction = (chinese_count // 4) * 0.02  # 每4个中文字符减少0.02个字符宽度
    english_reduction = (
        english_count // 20
    ) * 0.009  # 每20个英文字符减少0.009个字符宽度
    return chinese_reduction + english_reduction


# 步骤 1: 读取文件夹下所有的 `.ipynb` 文件
def get_all_ipynb_files(folder_path):
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".ipynb")
    ]


# 步骤 2: 将每个文件中的代码单元格内容转换为图片并保存到 `res` 文件夹
def convert_code_cells_to_images(ipynb_path, img_folder):
    with open(ipynb_path) as f:
        notebook = nbformat.read(f, as_version=4)

    img_paths = []
    for i, cell in enumerate(notebook.cells):
        if cell.cell_type == "code":
            # 根据代码行数调整图片大小
            lines = cell.source.split("\n")
            height = max(0, len(lines) * 0.2) + 0.3  # 调整行距和图片高度

            # 使用 Pygments 渲染代码
            highlighted_code = highlight(
                cell.source,
                PythonLexer(),
                HtmlFormatter(style="default", full=True, noclasses=True),
            )

            # 渲染代码单元格内容为图片
            fig, ax = plt.subplots(figsize=(12, height))  # 输出图片大小，12英寸
            fig.patch.set_facecolor(code_background_color)
            ax.set_facecolor(code_background_color)

            for spine in ax.spines.values():
                spine.set_visible(False)

            ax.set_xticks([])
            ax.set_yticks([])

            # 使用BeautifulSoup解析生成的HTML以确保高亮代码显示正确
            soup = BeautifulSoup(highlighted_code, "html.parser")
            pre_tag = soup.find("pre")
            code_lines = pre_tag.get_text().split("\n")

            # 设置行高因子
            line_height_factor = 1  # 可根据需要调整，>1增加行高，<1减少行高

            for j, line in enumerate(lines, start=1):
                x_offset = 0.06
                if line.lstrip().startswith("#"):
                    # 处理注释行
                    ax.text(
                        x_offset,
                        1 - j / (len(lines) + 1) * line_height_factor,
                        line,
                        fontsize=13,
                        va="top",
                        color=comment_color,
                    )
                else:
                    # 处理非注释行
                    in_string = False
                    quote_char = None
                    current_word = ""

                    for char in line:
                        if not in_string:
                            if char in ["'", '"']:
                                if current_word:
                                    color = (
                                        keyword_color
                                        if current_word in keywordlist
                                        else text_color
                                    )
                                    ax.text(
                                        x_offset,
                                        1 - j / (len(lines) + 1) * line_height_factor,
                                        current_word,
                                        fontsize=13,
                                        va="top",
                                        color=color,
                                    )
                                    x_offset += sum(
                                        get_char_width(c) for c in current_word
                                    )
                                    current_word = ""
                                in_string = True
                                quote_char = char
                                current_word = char
                            elif char.isdigit():
                                current_word += char
                            elif char.isalnum() or char == "_":
                                current_word += char
                            else:
                                if current_word:
                                    if current_word.isdigit():
                                        color = number_color
                                    else:
                                        color = (
                                            keyword_color
                                            if current_word in keywordlist
                                            else text_color
                                        )
                                    ax.text(
                                        x_offset,
                                        1 - j / (len(lines) + 1) * line_height_factor,
                                        current_word,
                                        fontsize=13,
                                        va="top",
                                        color=color,
                                    )
                                    x_offset += sum(
                                        get_char_width(c) for c in current_word
                                    )
                                    current_word = ""
                                color = (
                                    operator_color
                                    if char in operatorlist
                                    else text_color
                                )
                                ax.text(
                                    x_offset,
                                    1 - j / (len(lines) + 1) * line_height_factor,
                                    char,
                                    fontsize=13,
                                    va="top",
                                    color=color,
                                )
                                x_offset += get_char_width(char)
                        else:
                            current_word += char
                            if char == quote_char:
                                adjusted_spacing = calculate_adjusted_spacing(
                                    current_word
                                )
                                ax.text(
                                    x_offset,
                                    1 - j / (len(lines) + 1) * line_height_factor,
                                    current_word,
                                    fontsize=13,
                                    va="top",
                                    color=string_color,
                                )
                                x_offset += (
                                    sum(get_char_width(c) for c in current_word)
                                    - adjusted_spacing
                                )
                                in_string = False
                                quote_char = None
                                current_word = ""

                    # 处理行末尾未闭合的字符串或剩余的单词
                    if current_word:
                        if current_word.isdigit():
                            color = number_color
                        else:
                            color = string_color if in_string else text_color
                        ax.text(
                            x_offset,
                            1 - j / (len(lines) + 1) * line_height_factor,
                            current_word,
                            fontsize=13,
                            va="top",
                            color=color,
                        )

                # 添加行号
                ax.text(
                    0.01,
                    1 - j / (len(lines) + 1) * line_height_factor,
                    f"{j:>3}",
                    fontsize=13,
                    va="top",
                    color=line_number_color,
                )

            # 绘制垂直分割线
            ax.axvline(0.05, color=line_number_color, linewidth=0.5)

            plt.subplots_adjust(left=0.01, right=0.99, top=1, bottom=0)

            img_name = f'{os.path.basename(ipynb_path).replace(".ipynb", "").replace(" ", "_")}_cell_{i}.png'
            img_path = os.path.join(img_folder, img_name)
            plt.savefig(
                img_path, bbox_inches="tight", pad_inches=0.1, dpi=300
            )  # 输出图片
            plt.close(fig)
            img_paths.append(img_name)

    return img_paths


# 步骤 3: 在原代码单元格上方添加 Markdown 单元格显示图片
# 步骤 4: 清空原代码单元格内容，并新增代码单元
def modify_notebook(ipynb_path, img_paths):
    with open(ipynb_path) as f:
        notebook = nbformat.read(f, as_version=4)

    new_cells = []
    img_index = 0
    for cell in notebook.cells:
        if cell.cell_type == "code":
            img_name = img_paths[img_index]
            img_index += 1
            new_cells.append(
                new_markdown_cell(f'![]({os.path.join("codeimg", img_name)})')
            )
            cell.source = "# 代码练习区...\n\n"
        new_cells.append(cell)

    notebook.cells = new_cells
    return notebook


# 步骤 5: 将修改后的文件另存为原文件名加"_学员版"
def save_modified_notebook(notebook, original_path):
    new_path = original_path.replace(".ipynb", "_学员版.ipynb")
    with open(new_path, "w") as f:
        nbformat.write(notebook, f)


# 主函数
def process_notebooks(folder_path, img_folder):
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    ipynb_files = get_all_ipynb_files(folder_path)
    for ipynb_file in ipynb_files:
        img_paths = convert_code_cells_to_images(ipynb_file, img_folder)
        modified_notebook = modify_notebook(ipynb_file, img_paths)
        save_modified_notebook(modified_notebook, ipynb_file)


# 使用例子
folder_path = "/home/jovyan/work/00临时目录"  # 替换为包含 .ipynb 文件的文件夹路径
img_folder = "/home/jovyan/work/00临时目录/codeimg"  # 保存图片的文件夹路径
process_notebooks(folder_path, img_folder)
