import streamlit as st
import numpy as np

def get_trig_value(func, angle_rad):
    """주어진 함수와 라디안 각도에 대한 삼각함수 값을 반환합니다."""
    if func == "sin":
        return np.sin(angle_rad)
    elif func == "cos":
        return np.cos(angle_rad)
    elif func == "tan":
        # 탄젠트는 90도, 270도에서 정의되지 않으므로 처리
        if abs(np.cos(angle_rad)) < 1e-9: # 1e-9는 매우 작은 값으로, 부동 소수점 오차 처리
            return "정의되지 않음"
        return np.tan(angle_rad)
    return None

def format_value_latex(value):
    """삼각함수 값을 LaTeX 형식으로 반환합니다."""
    if isinstance(value, str):
        return value  # '정의되지 않음'과 같은 문자열은 그대로 반환
    
    # 정수 및 특정 분수/무리수 값은 정확한 LaTeX 표현 사용
    if np.isclose(value, 0):
        return r"0"
    elif np.isclose(value, 1):
        return r"1"
    elif np.isclose(value, -1):
        return r"-1"
    elif np.isclose(value, 0.5):
        return r"\frac{1}{2}"
    elif np.isclose(value, -0.5):
        return r"-\frac{1}{2}"
    elif np.isclose(value, np.sqrt(2)/2):
        return r"\frac{\sqrt{2}}{2}"
    elif np.isclose(value, -np.sqrt(2)/2):
        return r"-\frac{\sqrt{2}}{2}"
    elif np.isclose(value, np.sqrt(3)/2):
        return r"\frac{\sqrt{3}}{2}"
    elif np.isclose(value, -np.sqrt(3)/2):
        return r"-\frac{\sqrt{3}}{2}"
    elif np.isclose(value, np.sqrt(3)):
        return r"\sqrt{3}"
    elif np.isclose(value, -np.sqrt(3)):
        return r"-\sqrt{3}"
    elif np.isclose(value, 1/np.sqrt(3)):
        return r"\frac{\sqrt{3}}{3}" # 유리화된 형태로
    elif np.isclose(value, -1/np.sqrt(3)):
        return r"-\frac{\sqrt{3}}{3}" # 유리화된 형태로
    
    # 그 외의 값은 소수점 4째 자리까지 표시
    return f"{value:.4f}"

# 라디안 값을 LaTeX 문자열로 변환하는 헬퍼 함수
def get_latex_rad_display(rad_val):
    if np.isclose(rad_val, 0): return r"0"
    elif np.isclose(rad_val, np.pi/6): return r"\frac{\pi}{6}"
    elif np.isclose(rad_val, np.pi/4): return r"\frac{\pi}{4}"
    elif np.isclose(rad_val, np.pi/3): return r"\frac{\pi}{3}"
    elif np.isclose(rad_val, np.pi/2): return r"\frac{\pi}{2}"
    elif np.isclose(rad_val, 2*np.pi/3): return r"\frac{2\pi}{3}"
    elif np.isclose(rad_val, 3*np.pi/4): return r"\frac{3\pi}{4}"
    elif np.isclose(rad_val, 5*np.pi/6): return r"\frac{5\pi}{6}"
    elif np.isclose(rad_val, np.pi): return r"\pi"
    elif np.isclose(rad_val, 7*np.pi/6): return r"\frac{7\pi}{6}"
    elif np.isclose(rad_val, 5*np.pi/4): return r"\frac{5\pi}{4}"
    elif np.isclose(rad_val, 4*np.pi/3): return r"\frac{4\pi}{3}"
    elif np.isclose(rad_val, 3*np.pi/2): return r"\frac{3\pi}{2}"
    elif np.isclose(rad_val, 5*np.pi/3): return r"\frac{5\pi}{3}"
    elif np.isclose(rad_val, 7*np.pi/4): return r"\frac{7\pi}{4}"
    elif np.isclose(rad_val, 11*np.pi/6): return r"\frac{11\pi}{6}"
    elif np.isclose(rad_val, 2*np.pi): return r"2\pi"
    else: return rf"{rad_val:.4f} \text{{ rad}}" # 일반적인 라디안 값

st.set_page_config(layout="centered")

st.title("📏 삼각함수 값 확인 앱")
st.markdown("고등학교 2학년 학생들을 위한 삼각함수 값 확인 도우미입니다.")

st.sidebar.header("설정")

selected_func = st.sidebar.radio(
    "삼각함수를 선택하세요:",
    ("sin", "cos", "tan"),
    index=0,
)

angle_unit = st.sidebar.radio(
    "각도 단위를 선택하세요:",
    ("도 (Degrees)", "라디안 (Radians)"),
    index=0
)

st.markdown("---")
st.header("각도 선택")

# 3. 각도 리스트 생성 (30, 45, 60의 배수)
angles_deg_values = []
for i in range(0, 13):
    angles_deg_values.append(i * 30)
for i in range(1, 9):
    angles_deg_values.append(i * 45)
for i in range(1, 7):
    angles_deg_values.append(i * 60)

angles_deg_values = sorted(list(set(angles_deg_values)))

# --- 세션 상태 초기화 ---
if 'selected_angle_rad' not in st.session_state:
    initial_deg = 30
    initial_rad = np.deg2rad(initial_deg)
    
    st.session_state.selected_angle_rad = initial_rad
    st.session_state.deg_for_display = initial_deg
    st.session_state.rad_for_display_latex = get_latex_rad_display(initial_rad)
    st.session_state.current_selected_unit = "도 (Degrees)" 
# --- 세션 상태 초기화 끝 ---

# 각도 버튼 생성
# Streamlit의 columns는 컨테이너를 반환하므로, 리스트로 받아서 순회하며 사용합니다.
num_cols = 6
cols = st.columns(num_cols) 

for idx, deg_val in enumerate(angles_deg_values):
    rad_val = np.deg2rad(deg_val)

    # 현재 버튼이 들어갈 컬럼 선택
    with cols[idx % num_cols]: # idx를 num_cols로 나눈 나머지로 컬럼 인덱스를 결정하여 가로로 채웁니다.
        if angle_unit == "도 (Degrees)":
            button_label = rf"${deg_val}^\circ$"
        else: # 라디안 선택 시
            button_label = rf"${get_latex_rad_display(rad_val)}$"
        
        # 버튼을 누르면 세션 상태 업데이트
        if st.button(button_label, key=f"angle_{deg_val}_{angle_unit}"):
            st.session_state.selected_angle_rad = rad_val
            st.session_state.deg_for_display = deg_val
            st.session_state.rad_for_display_latex = get_latex_rad_display(rad_val)
            st.session_state.current_selected_unit = angle_unit
    
st.markdown("---")
st.header("계산 결과")

# 삼각함수 값 계산
trig_value = get_trig_value(selected_func, st.session_state.selected_angle_rad)
formatted_trig_value_latex = format_value_latex(trig_value)

# 결과 출력
st.markdown(f"선택한 삼각함수: **{selected_func}**")

# 선택된 각도와 반대 단위의 각도 표시
st.markdown(f"선택된 각도: ")
if st.session_state.current_selected_unit == "도 (Degrees)":
    # 도를 선택했으므로 라디안으로 표시
    st.latex(rf"\text{{입력 각도: }} {st.session_state.deg_for_display}^\circ \quad (\text{{라디안: }} {st.session_state.rad_for_display_latex})")
else:
    # 라디안을 선택했으므로 도로 표시
    st.latex(rf"\text{{입력 각도: }} {st.session_state.rad_for_display_latex} \quad (\text{{도: }} {st.session_state.deg_for_display}^\circ)")


st.markdown(f"") # 간격 조절
st.markdown("결과:")
st.latex(rf"\text{{{selected_func}}}({get_latex_rad_display(st.session_state.selected_angle_rad)}) = {formatted_trig_value_latex}") # 함수 인자에는 라디안 LaTeX 사용

st.markdown("---")
st.markdown("궁금한 삼각함수 값을 선택하고 각도를 변경하여 확인해보세요!")
