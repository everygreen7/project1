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
        min_value=0.1,
        max_value=10.0,
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

    phase_shift = st.sidebar.slider(
        "위상 이동 (C)",
        min_value=-np.pi,
        max_value=np.pi,
        value=0.0,
        step=0.1
    )

    vertical_shift = st.sidebar.slider(
        "수직 이동 (D)",
        min_value=-5.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    x_min = st.sidebar.slider(
        "X축 최소값",
        min_value=-10.0,
        max_value=0.0,
        value=-2 * np.pi,
        step=0.5
    )

    x_max = st.sidebar.slider(
        "X축 최대값",
        min_value=0.0,
        max_value=10.0,
        value=2 * np.pi,
        step=0.5
    )

    # X 값 생성
    x = np.linspace(x_min, x_max, 500)
    y = np.zeros_like(x)

    # 함수 계산
    if function_type == "sin(x)":
        y = amplitude * np.sin(frequency * x + phase_shift) + vertical_shift
        formula = f"$y = {amplitude:.2f} \sin({frequency:.2f}x + {phase_shift:.2f}) + {vertical_shift:.2f}$"
    elif function_type == "cos(x)":
        y = amplitude * np.cos(frequency * x + phase_shift) + vertical_shift
        formula = f"$y = {amplitude:.2f} \cos({frequency:.2f}x + {phase_shift:.2f}) + {vertical_shift:.2f}$"
    elif function_type == "tan(x)":
        # 탄젠트 함수는 특이점이 있으므로 주의
        y = amplitude * np.tan(frequency * x + phase_shift) + vertical_shift
        formula = f"$y = {amplitude:.2f} \tan({frequency:.2f}x + {phase_shift:.2f}) + {vertical_shift:.2f}$"
        # 탄젠트 그래프의 특이점을 처리하기 위한 마스킹 (옵션)
        # 문제가 발생하면 아래 주석 해제하여 사용
        # mask = np.abs(np.cos(frequency * x + phase_shift)) > 0.01 # 0에 가까워지는 값 필터링
        # y[~mask] = np.nan # 유효하지 않은 값은 NaN으로 설정하여 그래프에 그리지 않음

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
    ax.set_ylim(min(y) - 1, max(y) + 1) # y축 범위 자동 조정 (탄젠트 때문에 수동 조정 필요할 수도 있음)

    if function_type == "tan(x)":
        # 탄젠트 함수에 대한 y축 범위 조정
        ax.set_ylim(-10, 10) # 탄젠트의 경우 적절한 y축 범위 설정이 중요합니다.

    st.pyplot(fig)

    st.subheader("설명")
    st.write("""
    이 앱은 스트림릿을 사용하여 삼각함수 그래프를 그립니다.
    왼쪽 사이드바에서 다음 파라미터들을 조정하여 그래프의 모양을 변경할 수 있습니다:

    * **함수 선택**: `sin(x)`, `cos(x)`, `tan(x)` 중 하나를 선택합니다.
    * **진폭 (A)**: 그래프의 높낮이를 조절합니다. ($A$)
    * **주파수 (B)**: 파동의 밀도를 조절합니다. 값이 클수록 파동이 더 조밀해집니다. ($B$)
    * **위상 이동 (C)**: 그래프를 좌우로 이동시킵니다. 양수 값은 왼쪽으로 이동, 음수 값은 오른쪽으로 이동합니다. ($C$)
    * **수직 이동 (D)**: 그래프를 상하로 이동시킵니다. ($D$)
    * **X축 최소/최대값**: 그래프를 그릴 X축의 범위를 설정합니다.

    **일반적인 삼각함수 방정식:** $y = A \cdot \text{function}(B x + C) + D$
    """)

if __name__ == "__main__":
    main()
