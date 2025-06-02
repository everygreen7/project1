import streamlit as st
import openai
import os # API 키를 환경 변수에서 가져오기 위해 필요

# --- 1. OpenAI API 키 설정 (보안이 중요!) ---
# 방법 1: Streamlit secrets 사용 (권장)
# .streamlit/secrets.toml 파일에 다음 내용을 추가합니다:
# OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API 키가 설정되지 않았습니다. `.streamlit/secrets.toml` 파일을 확인해주세요.")
    st.stop() # 키가 없으면 앱 실행 중지

# 방법 2: 환경 변수 사용 (배포 시 유용)
# 터미널에서 export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
# 또는 .env 파일 사용 후 `python-dotenv` 라이브러리로 로드
# openai.api_key = os.getenv("OPENAI_API_KEY")
# if not openai.api_key:
#     st.error("OpenAI API 키가 환경 변수에 설정되지 않았습니다.")
#     st.stop()


# --- 2. Streamlit UI 설정 ---
st.title("삼각함수 LLM 챗봇 (OpenAI GPT)")

# 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 삼각함수 전문가 챗봇입니다. 삼각함수에 대한 질문에 친절하고 정확하게 답변해주세요. 수학 공식은 LaTeX 형식으로 표현해주세요. 예를 들어, sin^2θ + cos^2θ = 1 은 $\\sin^2\\theta + \\cos^2\\theta = 1$ 로 표현하세요."}
    ]
    # 사용자에게 보여줄 초기 메시지 (assistant 역할로)
    st.session_state.messages.append({"role": "assistant", "content": "안녕하세요! 삼각함수에 대해 무엇이든 물어보세요."})

# 대화 기록 표시
for message in st.session_state.messages:
    # 'system' 역할의 메시지는 화면에 표시하지 않습니다.
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 3. 챗봇 응답 로직 (OpenAI API 호출) ---
def get_openai_response(user_prompt):
    # 이전 대화 기록과 현재 사용자 프롬프트를 함께 전달
    # st.session_state.messages에는 system 프롬프트가 포함되어 있습니다.
    response = openai.chat.completions.create(
        model="gpt-4o",  # 또는 "gpt-3.5-turbo" 등 사용 가능한 모델
        messages=st.session_state.messages,
        temperature=0.7, # 창의성 조절 (0.0은 보수적, 1.0은 창의적)
        stream=True # 실시간 스트리밍 응답 활성화 (선택 사항, 사용자 경험 개선)
    )
    
    # 스트리밍 응답 처리
    full_response = ""
    message_placeholder = st.empty() # 응답이 표시될 빈 공간 생성
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌") # 커서 효과

    message_placeholder.markdown(full_response) # 최종 응답 표시
    return full_response

# 사용자 입력 처리
if prompt := st.chat_input("삼각함수에 대해 무엇이 궁금하신가요?"):
    # 사용자 메시지를 대화 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 챗봇 응답 생성 및 표시
    with st.chat_message("assistant"):
        # 스피너 표시
        with st.spinner("생각 중..."):
            try:
                ai_response = get_openai_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except openai.APIError as e:
                error_message = f"OpenAI API 호출 중 오류가 발생했습니다: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
            except Exception as e:
                error_message = f"예상치 못한 오류가 발생했습니다: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
