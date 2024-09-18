# TTF2WOFF 🖋️➡️🌐

TTF2WOFF 是一个用于批量将 TTF 字体文件转换为 WOFF 和 WOFF2 格式的 Python 脚本。该脚本支持子集化处理，保留指定的字符集，以减小字体文件大小。利用 Rich 库提供美观的进度条和日志输出。

## 特性 ✨

- **批量字体转换**：支持将多个 TTF 字体文件批量转换为 WOFF 和 WOFF2 格式
- **子集化处理**：可以指定保留的字符集，减少字体文件大小
- **美观的进度显示**：使用 Rich 库实时显示转换进度和状态
- **灵活配置**：通过 `config.py` 文件设置输入、输出目录、输出格式和子集字符集

## 环境要求 🛠️

- **Python 版本**：**`>= 3.12.1`**

## 使用方法 📦（推荐使用虚拟环境）

1. **克隆或下载项目**

    ```bash
    git clone https://github.com/Viper373/MagickTools.git
    cd MagickTools/ttf2woff
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

4. **配置 `config.py` 文件**

    在项目根目录下，创建或编辑 `config.py` 文件，内容如下：

    ```python
    TTF_DIR = "输入 TTF 字体文件的目录路径"
    WOFF_DIR = "输出 WOFF/WOFF2 字体文件的目录路径"
    OUTPUT_FORMATS = ["woff", "woff2"]  # 要输出的格式
    SUBSET_CHARS = "保留的字符集"  # 例如 "Hello World"
    ```

    **示例：**

    ```python
    TTF_DIR = "./ttf"
    WOFF_DIR = "./woff"
    OUTPUT_FORMATS = ["woff", "woff2"]
    SUBSET_CHARS = "你好，世界！1234567890"  # 添加更多字符以保留
    ```

5. **准备输入目录**

    将您想要转换的 TTF 字体文件放入 `TTF_DIR` 指定的目录中。脚本会遍历该目录下的所有 TTF 文件，并进行转换。

6. **运行脚本**

    ```bash
    python main.py
    ```

7. **查看输出**

    转换完成后，WOFF 和 WOFF2 字体文件将保存到 `WOFF_DIR` 指定的目录中。

## 代码结构 🗂️

- `main.py`：主脚本，负责读取配置、处理字体转换任务
- `config.py`：配置文件，用于设置输入输出目录、输出格式和子集字符集
- `requirements.txt`：依赖库列表

## 注意事项 ⚠️

- **依赖库**：请确保已安装 `fontTools` 和 `rich` 库（已在 `requirements.txt` 中列出）
- **子集化处理**：请根据需要设置 `SUBSET_CHARS`，以保留所需的字符，减少字体文件大小
- **字体版权**：请确保您有权转换和子集化所使用的字体文件
- **并行处理**：由于 Python 的 GIL（全局解释器锁），此脚本未使用多进程或多线程。如需处理大量文件，请自行优化

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

---

### 感谢使用！😊
