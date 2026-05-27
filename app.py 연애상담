import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 AI 상담")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ Secrets에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 시스템 프롬프트
SYSTEM_PROMPT = """
너는 공감 능력이 뛰어난 연애상담 전문 AI야.

규칙:
- 친절하고 따뜻하게 답변할 것
- 상대를 비난하지 말 것
- 현실적이고 구체적인 조언 제공
- 너무 단정짓지 말 것
- 사용자의 감정을 먼저 공감할 것
- 답변은 자연스럽고 대화체로 작성
"""

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("연애 고민을 이야기해보세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("생각 중이에요..."):

            try:
                # 이전 대화 기록 문자열 생성
                history_text = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "AI"
                    history_text += f"{role}: {msg['content']}\n"

                prompt = f"""
{SYSTEM_PROMPT}

아래는 이전 대화 내용이야.

{history_text}

이어서 자연스럽게 답변해줘.
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=500,
                    )
                )

                ai_response = response.text

                # 응답 출력
                st.markdown(ai_response)

                # 기록 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:
                error_message = f"""
⚠️ 오류가 발생했어요.

오류 내용:
`{str(e)}`

잠시 후 다시 시도해주세요.
"""

                st.error(error_message)
