# FastAPI + LangChain

本文案例使用 uv 管理项目，通过 FastAPI 的 POST /chat 接口接收问题，
再通过 LangChain 的 ChatOpenAI 调用 DeepSeek V4 Flash，返回 answer。
浏览器和本机都使用文章中的 create_agent，执行真正的 LangGraph 图。

## 文件与配置

- main.py：加载模型配置，创建 LangGraph Agent，定义 ChatRequest 和 POST /chat。
- .env：模型名称、OpenAI 兼容地址和你自己的 API Key。
- .env.example：不包含真实密钥的配置模板。
- pyproject.toml：项目依赖、Python 版本要求与 uv 配置。
- .python-version：本机使用 Python 3.12。
- .gitignore：忽略虚拟环境、缓存与本地密钥文件。

请打开 .env，将 DEEPSEEK_API_KEY=xxxx 中的 xxxx 替换为你自己的
DeepSeek API Key，然后保存并重新运行。xxxx 仅为占位符，不能用于调用模型。

使用 OpenAI 兼容中转服务时，修改 DEEPSEEK_BASE_URL。
不要将真实密钥填写到 .env.example 或提交到 Git。

## 浏览器运行

点击运行后，项目文件会写入 Pyodide 虚拟文件系统，安装声明的依赖，
运行环境读取项目根目录的 .env，再导入 main:app，与本机 uv --env-file 的配置方式一致。
请求通过 HTTPX ASGITransport 进入 FastAPI，
模型请求通过浏览器 Fetch 发出，不监听本机真实端口。

浏览器使用真正的 Python LangGraph，通过 agent.ainvoke 执行图。
网站提供与当前 Python / Pyodide ABI 匹配的 ormsgpack WASM 包；
LangChain 与 LangGraph 的 Python 包按项目依赖安装，并使用浏览器缓存。
无需在本机安装 Python，也不把案例转发到 Portal 执行。

浏览器通过 asyncio 执行图；请使用 ainvoke / astream。
普通同步节点和工具会在当前 Worker 中执行，不具备线程并行能力。
网络工具应使用异步 HTTPX / 浏览器 Fetch；本机 Socket、子进程和
原生数据库驱动仍不属于浏览器运行能力。检查点可使用 InMemorySaver，
重新运行或关闭页面会重建 Python 环境。

在案例预览中发送 POST /chat：

    {"question": "请用一句话介绍 LangChain。"}

成功后返回：

    {"answer": "模型的实际回复"}

main.py 与文章中的案例一致，使用 os.environ 读取配置。
修改代码或 .env 后都需要重新运行。
浏览器跨域规则也适用于模型请求；如果目标地址未允许当前网站的跨域请求，
请使用允许跨域的 OpenAI 兼容地址，或下载项目后在本机运行。

浏览器使用固定的 Python 3.14 环境，.python-version 不会改变该版本。
依赖通过 micropip 按需安装纯 Python wheel 或匹配当前 Pyodide ABI 的 WebAssembly wheel。
pyproject.toml 使用环境标记排除 FastAPI 本机服务器依赖，
并固定已经验证的 LangChain、LangGraph 与浏览器模型调用版本。
实际安装版本保存在 browser-python.lock.json，已下载的 wheel 使用浏览器缓存。
PI Agent 添加的依赖保存在 browser-requirements.txt，清单与锁文件应一起保存到 Git。

## 本机运行

下载项目 ZIP 并解压，在项目目录执行：

    uv python install 3.12
    uv venv --python 3.12
    uv sync

如果没有 .env，先复制 .env.example 为 .env，再填入你自己的 API Key。
启动方式与文章一致：

    uv run --env-file .env fastapi dev

服务启动后，在另一个终端发送请求：

    curl -X POST http://127.0.0.1:8000/chat \
      -H "Content-Type: application/json" \
      -d '{"question":"请用一句话介绍 LangChain。"}'

也可以打开 http://127.0.0.1:8000/docs 查看并测试接口。
uv sync 生成的 uv.lock 用于本机，浏览器使用自己的依赖锁文件。
如果项目有 browser-requirements.txt，在启动前执行
uv pip install -r browser-requirements.txt 安装 Agent 添加的依赖。
