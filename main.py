import streamlit as st
import random

# --- 0. 페이지 설정 (가장 먼저 실행되어야 함) ---
st.set_page_config(
    page_title="삼각함수 퀴즈 배틀! 📚",
    page_icon="📐",
    layout="centered", # wide 또는 centered
    initial_sidebar_state="collapsed" # 퀴즈 앱이므로 사이드바는 숨김
)

# --- CSS 스타일링 (배경색, 폰트 등) ---
st.markdown(
    """
    <style>
    /* 배경색 그라데이션 (고등학생들이 좋아할 만한 밝은 색상) */
    .stApp {
        background: linear-gradient(to right, #e0f2f7, #d4edda); /* 하늘색에서 연두색 그라데이션 */
        color: #333333; /* 기본 텍스트 색상 */
    }

    /* 제목 스타일 */
    h1 {
        color: #2c3e50; /* 진한 파란색 */
        text-align: center;
        font-size: 3.5em; /* 제목 크기 키우기 */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1); /* 그림자 효과 */
    }

    /* 부제목 (문제 번호) 스타일 */
    h2 {
        color: #2980b9; /* 파란색 */
        text-align: center;
        font-size: 2em;
    }

    /* 문제 텍스트 스타일 */
    h3 {
        color: #34495e; /* 진한 회색 */
        text-align: center;
        font-size: 1.8em;
        padding-bottom: 20px;
    }

    /* 라디오 버튼 텍스트 스타일 */
    .stRadio > label {
        font-size: 1.2em;
        margin-bottom: 10px; /* 보기 간 간격 추가 */
    }
    .stRadio div[role="radiogroup"] {
        padding: 10px;
        background-color: rgba(255,255,255,0.7); /* 반투명 흰색 배경 */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* 그림자 */
    }
    .stRadio div[role="radiogroup"] > label {
        padding: 8px 15px;
        border-radius: 8px;
        margin: 5px 0;
        transition: background-color 0.3s ease; /* 호버 효과 */
    }
    .stRadio div[role="radiogroup"] > label:hover {
        background-color: rgba(200, 200, 200, 0.3); /* 호버 시 배경색 변경 */
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #2ecc71; /* 에메랄드 그린 */
        color: white;
        font-size: 1.2em;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        display: block; /* 버튼 중앙 정렬을 위해 블록 요소로 변경 */
        margin: 20px auto; /* 중앙 정렬 */
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #27ae60; /* 호버 시 더 진한 그린 */
    }
    /* 점수 표시 */
    .st-emotion-cache-1jmvejs { /* st.write로 출력되는 요소의 클래스 (버전별로 다를 수 있음) */
        text-align: center;
        font-size: 1.5em;
        color: #3498db;
        font-weight: bold;
    }
    /* 정보/성공/오류 메시지 */
    .stAlert {
        text-align: center;
        font-size: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- 1. 퀴즈 문제 데이터 정의 ---
QUIZ_QUESTIONS = [
    {
        "question": r"$\cos(60^\circ)$의 값은 무엇인가요?",
        "answer": r"$1/2$",
        "options": [r"$1/2$", r"$\sqrt{3}/2$", r"$\sqrt{2}/2$", r"$0$"]
    },
    {
        "question": r"$\sin(30^\circ)$의 값은 무엇인가요?",
        "answer": r"$1/2$",
        "options": [r"$1/2$", r"$\sqrt{3}/2$", r"$\sqrt{2}/2$", r"$0$"]
    },
    {
        "question": r"$\tan(45^\circ)$의 값은 무엇인가요?",
        "answer": r"$1$",
        "options": [r"$1$", r"$0$", r"정의되지 않음", r"$\sqrt{3}$"]
    },
    {
        "question": r"다음 중 $\sin^2\theta + \cos^2\theta$ 와 항상 같은 값은 무엇인가요?",
        "answer": r"$1$",
        "options": [r"$1$", r"$0$", r"$\tan^2\theta$", r"$\sec^2\theta$"]
    },
    {
        "question": r"직각삼각형에서 빗변이 5이고 높이(대변)가 3일 때, $\sin$ 값은 무엇인가요?",
        "answer": r"$3/5$",
        "options": [r"$3/5$", r"$4/5$", r"$3/4$", r"$5/3$"]
    },
    {
        "question": r"사인 함수의 주기는 얼마인가요?",
        "answer": r"$2\pi$",
        "options": [r"$2\pi$", r"$\pi$", r"$\pi/2$", r"$4\pi$"]
    },
    {
        "question": r"탄젠트 함수가 정의되지 않는 $0^\circ$ ~ $360^\circ$ 사이의 각도는 무엇인가요?",
        "answer": r"$90^\circ$",
        "options": [r"$90^\circ$", r"$180^\circ$", r"$270^\circ$", r"$0^\circ$"]
    },
    {
        "question": r"$y = \sin(x)$ 그래프의 최댓값은 무엇인가요?",
        "answer": r"$1$",
        "options": [r"$1$", r"$0$", r"$-1$", r"$2$"]
    },
    # 여기에 새로운 문제 추가
    {
        "question": r"사인 함수의 최솟값은 얼마인가요?",
        "answer": r"$-1$",
        "options": [r"$-1$", r"$0$", r"$1$", r"$-2$"]
    }
]

# --- 2. Streamlit 앱 상태 관리 ---
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_questions_shuffled" not in st.session_state:
    st.session_state.quiz_questions_shuffled = []
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None
if "current_options_shuffled" not in st.session_state:
    st.session_state.current_options_shuffled = []


# 퀴즈 시작 함수
def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.quiz_questions_shuffled = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS)) # 문제 순서 섞기
    
    # 첫 번째 문제의 보기 순서 저장
    current_q = st.session_state.quiz_questions_shuffled[st.session_state.current_question_index]
    st.session_state.current_options_shuffled = random.sample(current_q["options"], len(current_q["options"]))

    st.session_state.show_feedback = False
    st.session_state.user_answer = None

# 다음 문제로 이동 함수
def next_question():
    st.session_state.show_feedback = False
    st.session_state.user_answer = None

    if st.session_state.current_question_index < len(st.session_state.quiz_questions_shuffled) - 1:
        st.session_state.current_question_index += 1
        current_q = st.session_state.quiz_questions_shuffled[st.session_state.current_question_index]
        st.session_state.current_options_shuffled = random.sample(current_q["options"], len(current_q["options"]))
    else:
        st.session_state.quiz_started = False
        st.session_state.current_question_index = 0
        st.session_state.quiz_questions_shuffled = []
        st.session_state.current_options_shuffled = []
        st.rerun()

# 답변 제출 함수
def submit_answer(selected_option):
    current_q = st.session_state.quiz_questions_shuffled[st.session_state.current_question_index]
    st.session_state.user_answer = selected_option
    st.session_state.show_feedback = True

    if selected_option == current_q["answer"]:
        st.session_state.score += 1
        st.success("정답입니다! 🎉 정답을 맞히다니, 최고! 😎")
    else:
        st.error(f"오답입니다. 😢 정답은 '{current_q['answer']}' 이에요! 다음엔 꼭 맞춰봐요! ✨")

# --- 3. 퀴즈 UI 렌더링 ---
if not st.session_state.quiz_started:
    st.info("삼각함수 지식을 테스트해 볼 시간! 🚀 지금 바로 퀴즈를 시작해 볼까요? 궁금하면 500원 말고 버튼 클릭! 😅")
    st.button("✨ 퀴즈 시작! ✨", on_click=start_quiz)

    if (st.session_state.current_question_index == 0 and
        not st.session_state.quiz_questions_shuffled and
        st.session_state.score > 0):
        st.balloons() # 퀴즈 종료 시 풍선 효과!
        st.success(
            f"🎉 퀴즈 종료! 🎉\n\n"
            f"총 {len(QUIZ_QUESTIONS)}문제 중 **{st.session_state.score}개**를 맞혔습니다!\n"
            f"정말 훌륭해요! 👍 계속 도전해서 삼각함수 마스터가 되어보세요! 🎓"
        )
        st.session_state.score = 0


else:
    current_q_index = st.session_state.current_question_index
    current_q = st.session_state.quiz_questions_shuffled[current_q_index]

    st.subheader(f"문제 {current_q_index + 1} / {len(QUIZ_QUESTIONS)} 🧐")
    st.markdown(r"### " + current_q["question"])

    options_to_display = st.session_state.current_options_shuffled

    selected_option = st.radio(
        "정답을 선택하세요:",
        options_to_display,
        index=options_to_display.index(st.session_state.user_answer) if st.session_state.user_answer in options_to_display else 0,
        key=f"question_radio_{current_q_index}"
    )

    if not st.session_state.show_feedback:
        st.button("✨ 정답 확인! ✨", on_click=submit_answer, args=(selected_option,))
    else:
        if st.session_state.current_question_index < len(st.session_state.quiz_questions_shuffled) - 1:
            st.button("➡️ 다음 문제! ➡️", on_click=next_question)
        else:
            st.button("✅ 퀴즈 종료! ✅", on_click=next_question)

    st.markdown(f"---")
    st.write(f"현재 점수: **{st.session_state.score}** / {current_q_index + 1} 💯")
