# MagicTools 🧰✨

一个自用工具类丨API

MagicTools 是一个由 Python 实现的实用工具集合，旨在简化日常工作流程，提升效率。每个工具都专注于特定的任务，如文件格式转换、批量处理等，利用 Python 的强大功能和丰富的库，为用户提供便捷的解决方案。

## 特性 ✨

- **多种实用工具**：包含 PDF 转 Word、目录压缩、PNG 转 ICO、TTF 转 WOFF、TXT 文件合并、`curl` 命令转换、IP 地址批量查询、SVG 编辑等多种工具。
- **批量处理支持**：大多数工具支持批量处理，节省时间和精力。
- **美观的进度显示**：使用 Rich 库实时显示进度条和状态更新。
- **灵活的配置**：通过配置文件设置输入、输出目录和其他参数。
- **可扩展性**：易于添加新的工具或功能，满足个性化需求。

## 包含的工具 🛠️

- **`curl2code`**：将 `curl` 命令转换为多种编程语言的代码，支持 Python、Java、Rust、Ruby 等。
- **`ip2multi`**：批量查询 `IP` 地址的地理位置信息，多线程支持，提高查询效率。
- **`svg1edit`**：简单的 `SVG` 文件编辑工具，支持批量处理和基本的图形操作。
- **`pdf2word`**：批量将 `PDF` 文件转换为 `Word` 文档。
- **`dir2zip`**：批量压缩目录为 `ZIP` 等格式。
- **`png2ico`**：批量将 `PNG` 图片转换为 `ICO` 图标文件。
- **`ttf2woff`**：批量将 `TTF` 字体文件转换为 `WOFF` 和 `WOFF2` 格式。
- **`txts2txt`**：批量合并 `TXT` 文件。

## 目录结构 📁

- `curl2code/`：包含 `curl2code` 工具的目录。
- `dir2zip/`：包含 `dir2zip` 工具的目录。
- `ip2multi/`：包含 `ip2multi` 工具的目录。
- `pdf2word/`：包含 `pdf2word` 工具的目录。
- `png2ico/`：包含 `png2ico` 工具的目录。
- `svg1edit/`：包含 `svg1edit` 工具的目录。
- `ttf2woff/`：包含 `ttf2woff` 工具的目录。
- `txts2txt/`：包含 `txts2txt` 工具的目录。
- `LICENSE`：许可证文件。

## 环境要求 🛠️

- **Python 版本**：**`>= 3.12.1`**

## 使用方法 📦（推荐使用虚拟环境）

1. **克隆或下载项目**

    ```bash
    git clone https://github.com/Viper373/MagickTools.git
    cd MagickTools
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

## TODO 📝

- **抛弃原生 HTML 和 CSS，前端使用 `Vue` 重构**：计划使用 `Vue.js` 框架重写前端界面，以提高开发效率和用户体验。
- **扩展 `curl2pro` 支持的编程语言**：添加对更多语言的支持，如 C#、PHP 等。
- **完善 `svg1edit` 的功能**：增加更多的 SVG 编辑功能，提升用户体验。

## 贡献指南 🤝

欢迎任何形式的贡献！如果您有新的工具、功能或改进建议，欢迎提交 `Pull Request`。一起让 MagicTools 变得更加完善。

## 反馈 🗣️

您的反馈对我们非常重要。如果您在使用过程中遇到任何问题，或者有任何建议，请随时与我们联系。

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: `2020311228@bipt.edu.cn`
- **GitHub**: [`Viper373`](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE) 文件。

---

### 感谢使用 MagicTools！😊
