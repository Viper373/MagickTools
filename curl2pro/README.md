# curl2pro 📡➡️💻

**curl2pro** 是一个用于将 `curl` 命令转换为多种编程语言代码的工具。支持多种语言，包括 Python、Java、Rust、Ruby 等，帮助开发者快速将 `curl` 请求集成到不同的编程环境中。通过 Rich 库提供美观的日志输出，提升用户体验。

## 特性 ✨

- **多语言支持**：支持将 `curl` 命令转换为 Python、Java、Rust、Ruby、Go、JavaScript、Node.js、Dart、Matlab、R 等多种编程语言。
- **灵活的参数解析**：支持解析 `curl` 命令中的各种参数，如请求方法、头部、数据、认证、代理等。
- **美观的日志输出**：使用 Rich 库实时显示解析和转换过程中的日志信息。
- **简洁易用**：通过命令行交互，轻松输入 `curl` 命令并选择目标语言进行转换。

## 环境要求 🛠️

- **Python 版本**：`>= 3.12.1`
- **依赖库**：
  - `requests`
  - `rich`

## 安装方法 📦（推荐使用虚拟环境）

1. **克隆或下载项目**

    ```bash
    git clone https://github.com/YourUsername/curl2pro.git
    cd curl2pro
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

## 使用方法 📜

1. **运行脚本**

    ```bash
    python main.py
    ```

2. **输入您的 `curl` 命令**

    在提示符下输入您需要转换的 `curl` 命令。例如：

    ```bash
    curl -X POST https://api.example.com/data -H "Content-Type: application/json" -d '{"key":"value"}'
    ```

3. **选择目标编程语言**

    选择您希望将 `curl` 命令转换为的编程语言。例如，选择 `Python`。

4. **查看生成的代码**

    转换完成后，生成的代码将以代码块形式显示在控制台中。您可以将其复制并集成到您的项目中。

## 代码结构 🗂️

- `converters/`：包含各个编程语言的转换器模块。
  - `__init__.py`
  - `base_converter.py`：所有转换器的基类。
  - `python_converter.py`：Python 代码转换器。
  - `java_converter.py`：Java 代码转换器。
  - `rust_converter.py`：Rust 代码转换器。
  - `ruby_converter.py`：Ruby 代码转换器。
  - `go_converter.py`：Go 代码转换器。
  - `javascript_converter.py`：JavaScript 代码转换器。
  - `nodejs_converter.py`：Node.js 代码转换器。
  - `dart_converter.py`：Dart 代码转换器。
  - `matlab_converter.py`：Matlab 代码转换器。
  - `r_converter.py`：R 代码转换器。
  - `json_converter.py`：JSON 格式转换器。
- `utils/`：实用工具模块。
  - `utils.py`：包含通用工具函数，如 `truncate_string`。
- `main.py`：主脚本，负责用户交互和调用相应的转换器。
- `requirements.txt`：依赖库列表。

## 示例

### 将 `curl` 命令转换为 Python 代码

**输入 `curl` 命令：**

```bash
curl -X POST https://api.example.com/data -H "Content-Type: application/json" -d '{"key":"value"}'
```
**选择目标语言：**
```markdown
请选择目标编程语言：
1. Python
2. Java
3. Rust
4. Ruby
5. Go
6. JavaScript
7. Node.js
8. Dart
9. Matlab
10. R
11. JSON
请输入数字 (默认: 1):
```
**输出转换后代码：**
```python
import requests

url = "https://api.example.com/data"
headers = {
    "Content-Type": "application/json",
}

json_data = {
    "key": "value"
}

response = requests.post(url,
    headers=headers,
    json=json_data,
    verify=True,
    allow_redirects=True
)

if response.status_code == 200:
    print("✅ 请求成功")
    print(response.text)
else:
    print(f"❌ 请求失败，状态码: {response.status_code}")
    print(response.text)
```

## 注意事项 ⚠️

- **依赖库**：请确保已安装 `rich` 库（已在 `requirements.txt` 中列出）
- **输入格式**：请确保输入的 `curl` 命令格式正确，避免解析错误。
- **输出文件**：当前版本不处理 `-o` 或 `--output` 参数，输出仅显示在控制台中。
- **安全性**：转换后的代码中包含`敏感信息（如认证信息）`时，请妥善保管和处理。

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

---

### 感谢使用！😊