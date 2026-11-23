# AI 助农助手

一个轻量的 Streamlit 对话应用，提供种植养护和常见病虫害的基础文字问答。

## 本地运行

1. 安装依赖：`pip install -r requirements.txt`
2. 创建 `.streamlit/secrets.toml`，填写自己的 DeepSeek API 密钥：

   ```toml
   deepseek_api_key = "填入你自己的 API 密钥"
   ```

3. 启动：`streamlit run app.py`

不要把 `.streamlit/secrets.toml` 或 API 密钥提交到 Git。

本应用提供一般性参考，不替代当地农技人员的诊断；农药、肥料使用请遵循产品标签和当地指导。
