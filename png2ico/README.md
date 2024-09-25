# PNG2ICO 🖼️➡️🖍️

PNG2ICO 是一个用于批量将 PNG 图片转换为多尺寸 ICO 图标的 Python 脚本。该脚本利用多进程并行处理，提高转换效率，并通过 Rich 库提供美观的进度条和日志输出。

## 特性 ✨

- **批量 PNG 转换**：支持将多个 PNG 图片批量转换为 ICO 图标文件
- **多尺寸图标支持**：生成包含多种常用尺寸的 ICO 文件（256x256、128x128、64x64 等）
- **多进程并行处理**：利用 `ProcessPoolExecutor` 提高转换速度
- **美观的进度显示**：使用 Rich 库实时显示转换进度和状态
- **灵活配置**：通过 `config.cfg` 文件设置输入、输出目录和并行进程数

## 使用方法 📦

1. **配置 `config.cfg` 文件**

   在项目根目录下，创建或编辑 `config.cfg` 文件，内容如下：

    ```ini
    [default]
    png_folder = 输入 PNG 图片的目录路径
    ico_folder = 输出 ICO 文件的目录路径
    max_worker = 最大并行进程数
    ```

   **示例：**

    ```ini
    [default]
    png_folder = ./png
    ico_folder = ./ico
    max_worker = 4
    ```

2. **准备输入目录**

   将您想要转换的 PNG 图片放入 `png_folder` 指定的目录中。脚本会遍历该目录下的所有 PNG 文件，并进行转换。

3. **运行脚本**

    ```bash
    cd png2ico
    python main.py
    ```

4. **查看输出**

   转换完成后，ICO 文件将保存到 `ico_folder` 指定的目录中。

## 代码结构 🗂️

- `main.py`：主脚本，负责读取配置、处理并行转换任务
- `config.cfg`：配置文件，用于设置输入输出目录和并行进程数
- `requirements.txt`：依赖库列表

## 注意事项 ⚠️

- **依赖库**：请确保已安装 `Pillow` 和 `rich` 库（已在 `requirements.txt` 中列出）
- **PNG 图片要求**：确保 PNG 图片为 RGBA 模式，以支持透明度
- **并行进程数**：`max_worker` 设置过大可能会占用大量系统资源，根据您的计算机性能进行调整

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

---

### 感谢使用！😊
