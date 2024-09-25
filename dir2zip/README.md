# Dir2Zip 📂➡️📁

Dir2Zip 是一个用于批量压缩目录的 Python 脚本，支持多种压缩格式，如 `zip`、`7z`、`rar`、`tar`、`gz` 等。该脚本利用多进程并行处理，提高压缩效率，并通过 Rich 库提供美观的进度条和日志输出。

## 特性 ✨

- **多种压缩格式支持**：`zip`、`7z`、`rar`、`tar`、`gz`、`gztar`、`bz2`、`bztar`、`xztar`
- **多进程并行压缩**：利用 `ProcessPoolExecutor` 提高压缩速度
- **美观的进度显示**：使用 Rich 库实时显示压缩进度和状态
- **灵活配置**：通过 `config.cfg` 文件设置输入、输出目录和并行进程数

## 使用方法 📦

1. 配置 config.cfg 文件
   在项目根目录下，创建或编辑 `config.cfg` 文件，内容如下：

    ```ini
    [default]
    input_folder = 输入目录的路径
    output_folder = 输出目录的路径
    max_worker = 最大并行进程数
    format = 默认压缩格式（如 zip）
    ```
   示例：
    ```ini
    [default]
    input_folder = ./input
    output_folder = ./output
    max_worker = 4
    format = zip
    ```
2. 准备输入目录
   将您想要压缩的子目录放入 `input_folder` 指定的目录中。脚本会遍历该目录下的所有子目录，并进行压缩。

3. 运行脚本
    ```bash
    cd dir2zip
    python main.py
    ```
4. 选择压缩格式
   运行脚本后，您会被提示输入压缩格式：
    ```text
    请输入压缩格式（现支持 zip, 7z, rar, tar, gz, gztar, bz2, bztar, xztar ，回车默认zip）：
    直接按回车：使用默认格式（在 config.cfg 中指定）
    输入格式：如 7z、rar 等，选择您需要的压缩格式
    ```
5. 查看输出
   压缩完成后，压缩文件将保存到 `output_folder` 指定的目录中。

## 代码结构 🗂️

- <code>main.py</code>：主脚本，负责读取配置、处理用户输入、并行压缩目录
- <code>compression_methods.py</code>：包含不同压缩格式的方法
- <code>config.cfg</code>：配置文件，用于设置输入输出目录、并行进程数和默认压缩格式
- <code>requirements.txt</code>：依赖库列表

## 注意事项 ⚠️

压缩格式支持：确保您的系统已安装所需的压缩工具。例如，使用 7z 格式，需要安装 7-Zip 工具。
Python 版本：请使用 Python <code>3.12.1</code> 或更高版本，以保证兼容性。
并行进程数：<code>max_worker</code> 设置过大可能会占用大量系统资源，根据您的计算机性能进行调整。

## 联系方式 📬

如有任何问题或建议，欢迎联系作者：

- **Email**: 2020311228@bipt.edu.cn
- **GitHub**: [Viper373](https://github.com/Viper373)

## 许可证 📄

本项目采用 MIT 许可证，详情请参阅 [LICENSE](../LICENSE) 文件。

### 感谢使用！😊