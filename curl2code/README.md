# curl2code 📡➡️💻

**curl2code** 是一个用于将 `curl` 命令转换为多种编程语言代码的工具。支持多种语言，包括 Python、Java、Rust、Ruby、Go、JavaScript、Node.js、Dart、MATLAB、R 等，帮助开发者快速将 `curl` 请求集成到不同的编程环境中。通过 `Rich` 库提供美观的日志输出，提升用户体验。

## 特性 ✨

- **多语言支持**：支持将 `curl` 命令转换为多种编程语言，包括：

  - **Python**（支持变体：`python`、`python-http`）
  - **Java**（支持变体：`java`、`java-httpurlconnection`、`java-jsoup`、`java-okhttp`）
  - **JavaScript**（支持变体：`javascript`、`javascript-jquery`、`javascript-xhr`）
  - **Node.js**（支持变体：`node`、`node-http`、`node-axios`、`node-got`、`node-ky`、`node-request`、`node-superagent`）
  - **PHP**（支持变体：`php`、`php-guzzle`、`php-requests`）
  - **PowerShell**（支持变体：`powershell`、`powershell-webrequest`）
  - **R**（支持变体：`r`、`r-httr2`）
  - **Ruby**（支持变体：`ruby`、`ruby-httparty`）
  - **Go**
  - **Rust**
  - **Dart**
  - **MATLAB**
  - **Swift**
  - **Kotlin**
  - **Lua**
  - **Perl**
  - **C#**
  - **C**
  - **Ansible**
  - **Objective-C**
  - **Elixir**
  - **Clojure**
  - **CFML**
  - **OCaml**
  - **JSON**
  - **HAR**
  - **HTTP**
  - **HTTPie**
  - **Wget**

- **灵活的参数解析**：利用 `curlconverter`，支持解析 `curl` 命令中的各种参数，如请求方法、头部、数据、认证、代理等。

- **美观的日志输出**：使用 `Rich` 库实时显示解析和转换过程中的日志信息。

- **简洁易用**：通过命令行交互，轻松输入 `curl` 命令并选择目标语言和变体进行转换。

## 安装 📥

**前置要求**：

- **`Python 3.12.1+`**
- **`Node.js 20+`**

## 使用方法 📦

1. **运行脚本**

    ```bash
    cd curl2code
    python main.py
    ```
2. **选择目标编程语言**

    运行脚本后，将显示支持的编程语言列表。输入对应的编号选择目标语言。
    例如，选择 `Python`，则输入`25`(默认)。
    示例：
    ```bash
    请选择目标编程语言：
    编号  语言
    1     Ansible
    2     C
    3     CFML
    4     Clojure
    5     C#
    6     Dart
    7     Elixir
    8     Go
    9     HAR
    10    HTTP
    11    HTTPie
    12    Java
    13    JavaScript
    14    JSON
    15    Julia
    16    Kotlin
    17    Lua
    18    MATLAB
    19    Node.js
    20    Objective-C
    21    OCaml
    22    Perl
    23    PHP
    24    PowerShell
    25    Python
    26    R
    27    Ruby
    28    Rust
    29    Swift
    30    Wget
    请输入数字（默认：25）:
    ```

3. **（可选）选择语言变体**

    对于具有多个变体的语言（如 Java、JavaScript、Python 等），程序会提示选择具体的变体。
    输入 `12` 选择 Java。
    输出：
    ```bash
    Java 有以下可选变体：
    1. java
    2. java-httpurlconnection
    3. java-jsoup
    4. java-okhttp
    请选择变体编号（默认：1）:
    ```
    输入 `4` 选择 `java-okhttp` 变体。

4. **输入您的 `curl` 命令**

    在提示符下输入您需要转换的 `curl` 命令。例如：

    - **`Python(requests)`**
   
    ```bash
    curl -X POST https://api.example.com/data -H "Content-Type: application/json" -d '{"key":"value"}'
    ```
   
    - **`Java(java-okhttp)`**
   
    ```bash
    curl -X GET https://api.example.com/data -H "Authorization: Bearer YOUR_TOKEN"
    ```

5. **查看生成的代码**

    转换完成后，生成的代码将以代码块形式显示在控制台中。
    示例：

    - **`Python(requests)`**
   
    ```python
    import requests

    url = 'https://api.example.com/data'
    headers = {
        'Content-Type': 'application/json',
    }
    
    json_data = {
        'key': 'value',
    }
    
    response = requests.post(url, headers=headers, json=json_data)
    ```
   
    - **`Java(java-okhttp)`**
   
    ```java
    OkHttpClient client = new OkHttpClient();

    Request request = new Request.Builder()
        .url("https://api.example.com/data")
        .get()
        .addHeader("Authorization", "Bearer YOUR_TOKEN")
        .build();

    Response response = client.newCall(request).execute();
    ```

## 代码结构 🗂️
- `curl2code/`：项目主目录
  - `converters/`：包含各个编程语言的转换器模块。
    - `__init__.py`
    - `base_converter.py`：所有转换器的基类。
    - `curl_converter_base.py`：封装 `curlconverter` 库的调用。
    - **各种编程语言的转换器，例如：
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
    - `fotmat.py`：包含通用工具函数，如 `truncate_string`。
    - `logger_util.py`：日志记录器，使用 `rich` 库美化输出。
  - `main.py`：主脚本，负责用户交互和调用相应的转换器。
- `requirements.txt`：Python依赖库列表。

## 注意事项 ⚠️

- **依赖库**：请确保`Python`、`Node.js`依赖
- **输入格式**：请确保输入的 `curl` 命令格式正确，避免解析错误。
- **语言支持**：由于使用 `curlconverter`，支持的语言和变体取决于 `curlconverter` 的版本。
- **安全性**：转换后的代码中包含`敏感信息（如认证信息）`时，请妥善保管和处理。

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

---

### 感谢使用！😊