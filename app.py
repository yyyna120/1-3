import streamlit as st
import google.generativeai as genai

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="AI 타로 챗봇",
    page_icon="🔮",
    layout="centered"
)

st.title("🔮 AI 타로 상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# ---------------------------
# API 키 불러오기
# ---------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# ---------------------------
# Gemini 설정
# ---------------------------
try:
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction="""
        너는 친절한 타로 상담사다.
        사용자의 고민을 공감하며 답변한다.
        답변은 너무 단정적으로 예언하지 말고,
        조언 중심으로 설명한다.
        말투는 부드럽고 따뜻하게 유지한다.
        """
    )

except Exception as e:
    st.error(f"모델 초기화 오류: {e}")
    st.stop()

# ---------------------------
# 채팅 기록 초기화
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 🔮 무엇이 고민이신가요? 타로 리딩을 도와드릴게요."
        }
    ]

# ---------------------------
# 기존 채팅 출력
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# 사용자 입력
# ---------------------------
user_input = st.chat_input("고민이나 질문을 입력하세요")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("타로 카드를 해석하는 중... 🔮"):

            try:
                # 대화 기록 구성
                history_text = ""

                for m in st.session_state.messages:
                    role = "사용자" if m["role"] == "user" else "상담사"
                    history_text += f"{role}: {m['content']}\n"

                prompt = f"""
                아래는 사용자와 타로 상담사의 대화 기록이다.

                {history_text}

                상담사로서 다음 답변을 작성해라.
                """

                response = model.generate_content(prompt)

                ai_response = response.text

            except Exception as e:
                ai_response = f"오류가 발생했습니다 😢\n\n{str(e)}"

            st.markdown(ai_response)

    # AI 메시지 저장
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

# ---------------------------
# 사이드바
# ---------------------------
with st.sidebar:
    st.header("🔮 안내")

    st.write("""
    - Gemini 2.5 Flash Lite 사용
    - 채팅 기록 유지
    - Streamlit Cloud 배포 가능
    """)

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "새로운 타로 상담을 시작할게요 🔮"
            }
        ]
        st.rerun()
