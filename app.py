import anthropic
import streamlit as st


MODEL = "deepseek-chat"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/anthropic"
SYSTEM_PROMPT = """你是一个务实、友好的 AI 助农助手，帮助用户解决常见种植养护问题。
回答前尽量确认作物、所在地区、生长阶段和症状；信息不足时先问一两个关键问题。
给出清晰、易执行的基础建议，不要编造诊断或具体农药、肥料用量。
涉及农药或肥料时，提醒用户严格遵守产品标签和当地农技部门指导；严重或快速扩散的问题建议联系当地农技人员。"""


def get_required_secret(name: str) -> str:
    try:
        value = st.secrets[name]
    except (FileNotFoundError, KeyError) as exc:
        raise RuntimeError(
            f"缺少密钥 `{name}`，请在 `.streamlit/secrets.toml` 中配置。"
        ) from exc

    secret = str(value).strip()
    if not secret:
        raise RuntimeError(f"密钥 `{name}` 为空，请检查配置。")
    return secret


def get_answer(messages: list[dict[str, str]]) -> str:
    client = anthropic.Anthropic(
        api_key=get_required_secret("deepseek_api_key"),
        base_url=DEEPSEEK_BASE_URL,
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=700,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    answer = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()
    if not answer:
        raise RuntimeError("模型没有返回文字内容，请稍后重试。")
    return answer


st.set_page_config(
    page_title="AI 助农助手",
    page_icon=":material/agriculture:",
    layout="centered",
)

st.title("AI 助农助手", icon=":material/agriculture:")
st.caption("种植养护与常见病虫害基础问答")

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.container(border=True):
        st.markdown("### 你好，我可以帮你一起看作物问题")
        st.write(
            "描述作物名称、所在地区、生长阶段和目前症状，"
            "我会先帮你梳理可能原因和基础处理思路。"
        )
        st.caption("例如：番茄定植后叶片发黄，最近浇水较多，应该先检查什么？")

for message in st.session_state.messages:
    avatar = ":material/person:" if message["role"] == "user" else ":material/agriculture:"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input(
    "描述你的作物、地区、生长期和遇到的问题…",
    submit_mode="disable",
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=":material/agriculture:"):
        try:
            with st.spinner("正在整理建议…"):
                answer = get_answer(st.session_state.messages)
            st.markdown(answer)
        except (RuntimeError, anthropic.APIError) as exc:
            st.error(f"暂时无法回答：{exc}")
        else:
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
