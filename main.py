import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.set_page_config(layout="wide")
    st.title("삼각함수 그래프 플로터")
    st.write("다양한 삼각함수 그래프를 직접 그려보세요!")

    # 사이드바 입력 설정
    st.sidebar.header("그래프 설정")

    function_type = st.sidebar.selectbox(
        "함수 선택",
        ("sin(x)", "cos(x)", "tan(x)")
    )

    amplitude = st.sidebar.slider(
        "진폭 (A)",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
        step=0.1
    )

    frequency = st.sidebar.slider(
        "주파수 (B)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1
    )

    x_shift = st.sidebar.slider(
        "X축 이동 (C)",
        min_value=-2 * np.pi,
        max_value=2 * np.pi,
        value=0.0,
        step=0.1
    )

    y_shift = st.sidebar.slider(
        "Y축 이동 (D)",
        min_value=-5.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    # X 값 생성 (고정 범위)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    y = np.zeros_like(x)

    # 함수 계산
    if function_type == "sin(x)":
        y = amplitude * np.sin(frequency * x + x_shift) + y_shift
        formula = f"$y = {amplitude:.2f} \sin({frequency:.2f}x + {x_shift:.2f}) + {y_shift:.2f}$"
    elif function_type == "cos(x)":
        y = amplitude * np.cos(frequency * x + x_shift) + y_shift
        formula = f"$y = {amplitude:.2f} \cos({frequency:.2f}x + {x_shift:.2f}) + {y_shift:.2f}$"
    elif function_type == "tan(x)":
        angle = frequency * x + x_shift
        y = amplitude * np.tan(angle) + y_shift
        formula = f"$y = {amplitude:.2f} \tan({frequency:.2f}x + {x_shift:.2f}) + {y_shift:.2f}$"
        # 탄젠트 함수 점근선 처리
        tolerance = 0.1
        y_masked = np.ma.masked_where(np.abs(np.cos(angle)) < tolerance, y)
        y = y_masked.filled(np.nan)

    st.subheader("그래프")
    st.markdown(f"**현재 함수:** {formula}")

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, color='blue')
    ax.set_xlabel("X축")
    ax.set_ylabel("Y축")
    ax.set_title(f"{function_type} 그래프")
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.8) # x축
    ax.axvline(0, color='black', linewidth=0.8) # y축
    ax.spines['top'].set_visible(False)    # 위쪽 테두리 제거
    ax.spines['right'].set_visible(False)  # 오른쪽 테두리 제거
    ax.set_ylim(-5, 5) # 고정된 Y축 범위

    if function_type == "tan(x)":
        # 점근선 표시 (끊어진 선으로 표현)
        cos_val = np.cos(frequency * x + x_shift)
        tan_x = frequency * x + x_shift
        for i in np.where(np.diff(np.sign(cos_val))):
            x_val = (tan_x [i] + tan_x [i+1]) / 2
            ax.plot([x_val, x_val], [-5, 5], color='red', linestyle='--', linewidth=1)


    st.pyplot(fig)

    st.subheader("설명")
    st.write("""
    이 앱은 스트림릿을 사용하여 삼각함수 그래프를 그립니다.
    왼쪽 사이드바에서 다음 파라미터들을 조정하여 그래프의 모양을 변경할 수 있습니다:

    * **함수 선택**: `sin(x)`, `cos(x)`, `tan(x)` 중 하나를 선택합니다.
    * **진폭 (A)**: 그래프의 높낮이를 조절합니다. (범위: 0 ~ 5)
    * **주파수 (B)**: 파동의 밀도를 조절합니다. 값이 클수록 파동이 더 조밀해집니다.
    * **X축 이동 (C)**: 그래프를 좌우로 이동시킵니다. 양수 값은 오른쪽으로 이동, 음수 값은 왼쪽으로 이동합니다.
    * **Y축 이동 (D)**: 그래프를 상하로 이동시킵니다.

    **일반적인 삼각함수 방정식:** $y = A \cdot \text{function}(B x + C) + D$
    """)

if __name__ == "__main__":
    main()
