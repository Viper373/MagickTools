# TXTs2TXT 📄➡️📑

MergeTXT 是一个用于批量合并 `.txt` 文件的 Python 脚本。该脚本可以将指定目录下的所有文本文件合并为一个文件，并支持自定义文件模式和覆盖选项。通过 Rich 库提供美观的进度条和日志输出。

## 特性 ✨

- **批量 TXT 文件合并**：支持将多个 `.txt` 文件合并为一个文件
- **自定义文件模式**：通过配置文件设置要匹配的文件模式（例如 `*.txt`、`*.log` 等）
- **美观的进度显示**：使用 Rich 库实时显示合并进度和状态
- **灵活配置**：通过 `config.cfg` 文件设置输入、输出目录、文件模式和覆盖选项

## 使用方法 📦

1. **配置 `config.cfg` 文件**

   在项目根目录下，创建或编辑 `config.cfg` 文件，内容如下：

    ```ini
    [default]
    input_directory = 输入文本文件的目录路径
    output_directory = 输出合并文件的目录路径
    file_pattern = 文件匹配模式，例如 *.txt
    log_file = 日志文件的路径
    overwrite = 是否覆盖已有的输出文件，True 或 False
    ```

   **示例：**

    ```ini
    [default]
    input_directory = ./input
    output_directory = ./output
    file_pattern = *.txt
    log_file = logs/merge.log
    overwrite = True
    ```

2. **准备输入目录**

   将您想要合并的 `.txt` 文件放入 `input_directory` 指定的目录中。脚本会根据 `file_pattern` 匹配文件，并进行合并。

3. **运行脚本**

    ```bash
    cd txts2txt
    python main.py
    ```

4. **查看输出**

   合并完成后，合并的文件将保存到 `output_directory` 指定的目录中，文件名格式为 `merged_X.txt`，其中 `X` 为自增的数字。

## 代码结构 🗂️

- `main.py`：主脚本，负责读取配置、处理合并任务
- `config.cfg`：配置文件，用于设置输入输出目录、文件模式和覆盖选项
- `requirements.txt`：依赖库列表

## 注意事项 ⚠️

- **依赖库**：请确保已安装 `rich` 库（已在 `requirements.txt` 中列出）
- **文件模式**：请根据需要设置 `file_pattern`，以匹配要合并的文件类型
- **覆盖选项**：`overwrite` 设置为 `True` 时，会覆盖已有的输出文件，请谨慎使用
- **日志文件**：日志将记录在 `log_file` 指定的路径，可用于调试和查看运行情况

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

---

### 感谢使用！😊
