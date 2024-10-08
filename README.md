# nbcode-to-img：Jupyter Notebook 学员版生成工具

该项目通过 Python 脚本将 Jupyter Notebook 文件中的代码单元格转换为图片，并插入到对应的 Markdown 单元格中，同时保留学员的代码练习区域，生成适合教学使用的学员版 Jupyter Notebook。

功能简介

	1.	自动识别 .ipynb 文件：读取指定文件夹中的所有 Jupyter Notebook 文件。
	2.	代码转换为图片：将每个代码单元格的内容渲染为图片并保存。
        3.      对代码进行高亮处理并生成图片。
	4.	添加 Markdown 单元格：在代码单元格上方插入对应的图片展示代码。
	5.	保留代码练习区域：清空原代码单元格的内容，保留提示信息以供学员填写代码。
	6.	生成学员版 Notebook：修改后的文件将以 _学员版 后缀保存，供学员练习使用。

安装依赖

请确保您的环境中已安装以下依赖项：

`pip install matplotlib nbformat beautifulsoup4 pygments`

使用说明

	1.	将项目克隆或下载到本地：

`git clone https://github.com/zengqueling/nbcode-to-img.git`

	2.	修改脚本中的路径参数，设置 Jupyter Notebook 文件所在的文件夹路径和图片保存路径：
```
folder_path = "/path/to/your/notebooks"  # 替换为包含 .ipynb 文件的文件夹路径
img_folder = "/path/to/save/images"  # 保存代码图片的文件夹路径
```
	3.	运行脚本，将代码单元格转换为图片并生成学员版文件：

`python generate_student_version.py`

	4.	转换后的 Notebook 文件将在原目录中生成，并附带 _学员版 后缀。

示例

转换前：
```python
# 示例代码单元格
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
```
转换后：
> 
	代码练习区…
学员可在此处输入代码进行练习。

主要参数与自定义选项

	•	字体设置：默认使用 YaHei Consolas Hybrid 字体以确保中英文混排显示效果良好。
	•	颜色主题：可自定义代码高亮配色，包括注释、关键字、运算符、字符串、数字等的颜色设置。
	•	行高调整：通过 line_height_factor 参数调整代码图片中的行高。
	•	字符宽度调整：基于中英文字符宽度，代码中的字符间距将自动调整，保证排版整齐。

项目结构
```
├── generate_student_version.py     # 主脚本
├── YaHei Consolas Hybrid 1.12.ttf  # 使用 YaHei Consolas Hybrid 字体以确保中英文混排显示效果良好
└── README.md                       # 项目说明文件
```

贡献

如果你对该项目有任何改进建议或发现了问题，欢迎提交 issue 或 Pull Request。

许可证

该项目遵循 MIT 许可证。

根据实际情况，你可以替换其中的路径及 GitHub 地址，内容也可以根据你的需求进行调整。
