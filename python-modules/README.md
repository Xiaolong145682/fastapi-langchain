# Python 模块与包

本案例对应第二篇文章，将问候逻辑、模型配置、提示词和 Agent 放进独立模块。
main.py 是 FastAPI 入口，app/__init__.py 声明普通 Python 包。

## 先运行无需密钥的模块示例

点击运行，然后发送默认的 GET /hello?name=小微。
main.py 从 greeting.py 导入常量与 Greeter，返回问候语及 DEFAULT_GREETING。
修改 greeting.py 中的 DEFAULT_GREETING，保存并重新运行，再发送请求即可观察变化。
greeting.py 中的 __all__ 约定公开名称，前导下划线表示内部辅助函数；
__name__ 判断让文件被导入时不会自动执行 main() 中的打印。

## 再运行 LangChain Agent

在 .env 中将 DEEPSEEK_API_KEY=xxxx 的 xxxx 替换为自己的密钥。
保存后重新运行，把请求方法改为 POST，地址改为 /chat，请求体填写：

    {"question": "请用一句话介绍 Python 模块。"}

main.py 调用 app.agent.get_agent；app.agent 使用相对导入读取
app.model.create_model 和 app.prompts.SYSTEM_PROMPT。
get_agent 首次调用时创建并缓存 Agent，后续请求复用；重新运行项目会重新加载模块。
这里使用真实的 LangChain create_agent 和 LangGraph ainvoke，不模拟模型回复。

不要将真实密钥填写到 .env.example 或推送到 Git。
模型请求由浏览器直连配置的 API 地址，该地址需要允许网站的跨域请求。

## 本机运行

在解压后的项目根目录执行：

    uv run python greeting.py
    uv run --env-file .env fastapi dev main.py

单独运行 greeting.py 会输出问候语。FastAPI 服务默认监听 8000 端口，
GET /hello 无需模型密钥；POST /chat 需要有效密钥。
包内模块需要单独运行时使用 uv run python -m app.agent，
不要直接执行 python app/agent.py；本模块只定义函数，不会自动调用模型。

## 浏览器运行约定

运行环境通过导入 main:app 加载项目，因此 main.py 的 __name__ 是 main。
浏览器不会执行 uv 或启动本机端口，请求通过 HTTPX ASGITransport 进入 FastAPI。
Python 固定为当前 Pyodide 的版本，.python-version 仅供本机 uv 使用。
依赖从 pyproject.toml 安装，wheel 下载缓存与同站其他文章共享，
代码、日志、Git 设置和 PI Agent 对话使用本篇独立的工作区存储。
LangGraph 使用异步 ainvoke / astream，不使用本机线程、子进程或 Socket。
