import streamlit as st
import random

# --- 1. 퀴즈 문제 데이터 정의 ---
# 문제, 정답, 오답 보기를 딕셔너리 리스트로 정의합니다.
# 보기 순서는 매번 랜덤하게 섞이도록 할 것입니다.
QUIZ_QUESTIONS = [
    {
        "question": "$\\sin(30^\\circ)$의 값은 무엇인가요?", # LaTeX 적용
        "answer": "1/2",
        "options": ["1/2", "루트3/2", "루트2/2", "0"]
    },
    {
        "question": "$\\cos(60^\\circ)$의 값은 무엇인가요?", # LaTeX 적용
        "answer": "1/2",
        "options": ["1/2", "루트3/2", "루트2/2", "1"]
    },
    {
        "question": "$\\tan(45^\\circ)$의 값은 무엇인가요?", # LaTeX 적용
        "answer": "1",
        "options": ["1", "0", "정의되지 않음", "루트3"]
    },
    {
        "question": "다음 중 $\\sin^2\\theta + \\cos^2\\theta$ 와 항상 같은 값은 무엇인가요?", # LaTeX 적용
        "answer": "1",
        "options": ["1", "0", "tan^2θ", "sec^2θ"]
    },
    {
        "question": "직각삼각형에서 빗변이 5이고 높이(대변)가 3일 때, $\\sin$ 값은 무엇인가요?", # LaTeX 적용
        "answer": "3/5",
        "options": ["3/5", "4/5", "3/4", "5/3"]
    },
    {
        "question": "사인 함수의 주기는 얼마인가요?",
        "answer": "2π",
        "options": ["2π", "π", "π/2", "4π"]
    },
    {
        "question": "탄젠트 함수가 정의되지 않는 각도는 무엇인가요? ($0^\\circ$ ~ $360^\\circ$ 사이)", # LaTeX 적용
        "answer": "90°",
        "options": ["90°", "180°", "270°", "0°"]
    },
    {
        "question": "$y = \\sin(x)$ 그래프의 최댓값은 무엇인가요?",
        "answer": "1",
        "options": ["1", "0", "-1", "2"]
    },
    {
        "question": "$\\tan \\theta = \\frac{\\sin \\theta}{\\cos \\theta}$ 는 어떤 관계를 나타내나요?",
        "answer": "탄젠트의 정의",
        "options": ["탄젠트의 정의", "사인 함수의 정의", "코사인 함수의 정의", "피타고라스 정리"]
    },
    {
        "question": "각도 $A$에 대해 $\\sec A$는 무엇의 역수인가요?",
        "answer": "cos A",
        "options": ["sin A", "cos A", "tan A", "cot A"]
    }
]

# --- 2. Streamlit 앱 설정 ---
st.title("삼각함수 퀴즈")

# 퀴즈 상태 초기화
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
    # 정답 피드백 초기화
    st.session_state.show_feedback = False
    st.session_state.user_answer = None

    if st.session_state.current_question_index < len(st.session_state.quiz_questions_shuffled) - 1:
        st.session_state.current_question_index += 1
        # 다음 문제의 보기 순서 새로 저장
        current_q = st.session_state.quiz_questions_shuffled[st.session_state.current_question_index]
        st.session_state.current_options_shuffled = random.sample(current_q["options"], len(current_q["options"]))
    else:
        # 모든 문제를 다 풀었을 경우 퀴즈 종료
        st.session_state.quiz_started = False
        st.session_state.current_question_index = 0 # 인덱스 초기화
        st.session_state.quiz_questions_shuffled = [] # 퀴즈 종료 시 문제 목록 초기화
        st.session_state.current_options_shuffled = [] # 퀴즈 종료 시 보기 목록 초기화
        st.rerun() # 퀴즈 종료 화면으로 리로드

# 답변 제출 함수
def submit_answer(selected_option):
    current_q = st.session_state.quiz_questions_shuffled[st.session_state.current_question_index]
    st.session_state.user_answer = selected_option
    st.session_state.show_feedback = True

    if selected_option == current_q["answer"]:
        st.session_state.score += 1
        st.success("정답입니다! 🎉")
    else:
        st.error(f"오답입니다. 정답은 '{current_q['answer']}' 입니다. 😢")

# --- 3. 퀴즈 UI 렌더링 ---
if not st.session_state.quiz_started:
    st.info("삼각함수 지식을 테스트해 보세요!")
    st.button("퀴즈 시작", on_click=start_quiz)

    # 퀴즈가 끝나고 다시 시작할 때 점수 표시
    if (st.session_state.current_question_index == 0 and
        not st.session_state.quiz_questions_shuffled and
        st.session_state.score > 0):
        st.success(f"퀴즈가 종료되었습니다! 총 {len(QUIZ_QUESTIONS)}문제 중 {st.session_state.score}개를 맞혔습니다. 훌륭해요!")
        st.session_state.score = 0


else:
    current_q_index = st.session_state.current_question_index
    current_q = st.session_state.quiz_questions_shuffled[current_q_index]

    st.subheader(f"문제 {current_q_index + 1} / {len(QUIZ_QUESTIONS)}")
    # st.markdown()을 사용하여 LaTeX 수식을 렌더링합니다.
    # r"..." (원시 문자열)을 사용하여 백슬래시 문제를 방지합니다.
    st.markdown(r"**" + current_q["question"] + r"**")

    # 보기를 섞어서 보여줍니다.
    options_to_display = st.session_state.current_options_shuffled

    # 라디오 버튼으로 보기 표시
    selected_option = st.radio(
        "정답을 선택하세요:",
        options_to_display,
        index=options_to_display.index(st.session_state.user_answer) if st.session_state.user_answer in options_to_display else 0,
        key=f"question_radio_{current_q_index}"
    )

    # 정답 제출 버튼
    if not st.session_state.show_feedback:
        st.button("정답 확인", on_click=submit_answer, args=(selected_option,))
    else:
        if st.session_state.current_question_index < len(st.session_state.quiz_questions_shuffled) - 1:
            st.button("다음 문제", on_click=next_question)
        else:
            st.button("퀴즈 종료", on_click=next_question)

    st.markdown(f"---")
    st.write(f"현재 점수: {st.session_state.score} / {current_q_index + 1}")
