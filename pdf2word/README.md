# PDF2Word 📄➡️📝

PDFConverter 是一个用于批量将 PDF 文件转换为 Word 文档的 Python 脚本。该脚本利用多进程并行处理，提高转换效率，并通过 Rich 库提供美观的进度条和日志输出。

## 特性 ✨

- **批量 PDF 转换**：支持将多个 PDF 文件批量转换为 Word 文档
- **多进程并行处理**：利用 `ProcessPoolExecutor` 提高转换速度
- **美观的进度显示**：使用 Rich 库实时显示转换进度和状态
- **灵活配置**：通过 `config.cfg` 文件设置输入、输出目录和并行进程数

## 使用方法 📦

1. **配置 `config.cfg` 文件**

   在项目根目录下，创建或编辑 `config.cfg` 文件，内容如下：

    ```ini
    [default]
    pdf_folder = 输入 PDF 文件的目录路径
    word_folder = 输出 Word 文件的目录路径
    max_worker = 最大并行进程数
    ```

   **示例：**

    ```ini
    [default]
    pdf_folder = ./pdf
    word_folder = ./word
    max_worker = 4
    ```

2. **准备输入目录**

   将您想要转换的 PDF 文件放入 `pdf_folder` 指定的目录中。脚本会遍历该目录下的所有 PDF 文件，并进行转换。

3. **运行脚本**

    ```bash
    cd pdf2word
    python main.py
    ```

4. **查看输出**

   转换完成后，Word 文档将保存到 `word` 指定的目录中。

## 代码结构 🗂️

- `main.py`：主脚本，负责读取配置、处理并行转换任务
- `config.cfg`：配置文件，用于设置输入输出目录和并行进程数
- `requirements.txt`：依赖库列表

## 注意事项 ⚠️

- **依赖库**：请确保已安装 `pdf2docx` 和 `rich` 库（已在 `requirements.txt` 中列出）
- **PDF 文件兼容性**：某些复杂的 PDF 文件可能无法完美转换为 Word 文档
- **并行进程数**：`max_worker` 设置过大可能会占用大量系统资源，根据您的计算机性能进行调整

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

---

### 感谢使用！😊
