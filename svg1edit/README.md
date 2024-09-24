# SVG1Edit ✏️📐

ModifySVG 是一个用于批量修改 `.svg` 文件尺寸的 Python 脚本。该脚本可以将指定目录下的所有 SVG 文件的宽度和高度进行调整，并支持自定义文件模式、默认尺寸以及覆盖选项。通过 Rich 库提供美观的进度条和日志输出，提升用户体验。

## 特性 ✨

- **批量 SVG 文件修改**：支持将多个 `.svg` 文件的宽度和高度批量修改为指定尺寸
- **自定义文件模式**：通过配置文件设置要匹配的文件模式（例如 `*.svg`、`*.xml` 等）
- **美观的进度显示**：使用 Rich 库实时显示修改进度和状态
- **灵活配置**：通过 `config.cfg` 文件设置输入、输出目录、文件模式、默认尺寸和覆盖选项
- **日志记录**：详细记录修改过程中的信息和错误，便于调试和审查

## 环境要求 🛠️

- **Python 版本**：**`>= 3.12.1`**

## 使用方法 📦（推荐使用虚拟环境）

1. **克隆或下载项目**

    ```bash
    git clone https://github.com/Viper373/MagickTools.git
    cd MagickTools/svg1edit
    ```

2. **创建并激活虚拟环境**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3. **安装依赖**

    ```bash
    pip install -r requirements.txt
    ```

4. **配置 `config.cfg` 文件**

    在项目根目录下，创建或编辑 `config.cfg` 文件，内容如下：

    ```ini
    [default]
    input_directory = 输入 SVG 文件的目录路径
    output_directory = 输出修改后文件的目录路径
    file_pattern = 文件匹配模式，例如 *.svg
    log_file = 日志文件的路径
    overwrite = 是否覆盖已有的输出文件，True 或 False
    new_width = 默认新的宽度
    new_height = 默认新的高度
    ```

    **示例：**

    ```ini
    [default]
    input_directory = ./input_svgs
    output_directory = ./output_svgs
    file_pattern = *.svg
    log_file = logs/modify_svg.log
    overwrite = True
    new_width = 800
    new_height = 600
    ```

5. **准备输入目录**

    将您想要修改尺寸的 `.svg` 文件放入 `input_directory` 指定的目录中。脚本会根据 `file_pattern` 匹配文件，并进行修改。

6. **运行脚本**

    ```bash
    python main.py
    ```

7. **查看输出**

    修改完成后，新的 SVG 文件将保存到 `output_directory` 指定的目录中，文件名格式为 `new_<原文件名>.svg`。例如，`logo.svg` 将被保存为 `new_logo.svg`。

## 代码结构 🗂️

- `main.py`：主脚本，负责读取配置、处理修改任务
- `config.cfg`：配置文件，用于设置输入输出目录、文件模式、默认尺寸和覆盖选项
- `requirements.txt`：依赖库列表

## 注意事项 ⚠️

- **依赖库**：请确保已安装 `rich` 库（已在 `requirements.txt` 中列出）
- **文件模式**：请根据需要设置 `file_pattern`，以匹配要修改的文件类型
- **覆盖选项**：`overwrite` 设置为 `True` 时，会覆盖已有的输出文件，请谨慎使用
- **日志文件**：日志将记录在 `log_file` 指定的路径，可用于调试和查看运行情况
- **SVG 文件格式**：确保待修改的 SVG 文件具有明确的 `width` 和 `height` 属性，以便脚本正确解析和修改

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

---

### 感谢使用！😊
