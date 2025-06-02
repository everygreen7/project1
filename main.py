import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker # ticker 모듈 추가

def main():
    st.set_page_config(layout="wide")
    st.title("삼각함수 그래프 플로터")
    st.write("다양한 삼각함수 그래프를 직접 그려보세요!")

    # 사이드바 입력 설정
    st.sidebar.header("그래프 설정")

    function_type = st.sidebar.radio(
        "함수 선택",
        ("sin(x)", "cos(x)", "tan(x)")
    )

    amplitude = st.sidebar.slider(
        "진폭 (A)",
        min_value=0.0,
        max_value=4.0,
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
    x_min_plot = -2 * np.pi
    x_max_plot = 2 * np.pi
    x = np.linspace(x_min_plot, x_max_plot, 500)
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
    ax.axhline(0, color='black', linewidth=1.5) # x축 (y=0에 표현)
    ax.axvline(0, color='black', linewidth=0.8) # y축
    ax.spines['top'].set_visible(False)    # 위쪽 테두리 제거
    ax.spines['right'].set_visible(False)  # 오른쪽 테두리 제거
    ax.set_ylim(-8, 8) # Y축 범위 -8~8로 변경
    ax.set_xlim(x_min_plot, x_max_plot) # X축 범위 설정

    # X축 눈금을 파이/4의 배수로 설정 및 라디안으로 표기
    # 파이/4 간격으로 주요 눈금 설정
    major_locator = ticker.MultipleLocator(np.pi / 4)
    ax.xaxis.set_major_locator(major_locator)

    # 눈금 라벨 포맷터 정의
    def format_func(value, tick_pos):
        if value == 0:
            return "0"
        
        num = value / np.pi
        
        # 작은 부동 소수점 오차를 처리하기 위해 반올림
        num_fraction = num * 4 
        round_num = round(num_fraction) 
        
        if abs(num_fraction - round_num) < 1e-9: 
            num = round_num / 4.0 
        
        if num == 1:
            return r"$\pi$"
        elif num == -1:
            return r"$-\pi$"
        elif num % 1 == 0: # 정수 파이 (예: 2pi)
            return r"${}\pi$".format(int(num))
        else: # 분수 파이 (예: pi/2, 3pi/4)
            numerator = int(num * 4) 
            denominator = 4
            
            gcd_val = np.gcd(numerator, denominator)
            numerator //= gcd_val
            denominator //= gcd_val
            
            if denominator == 1:
                return r"${}\pi$".format(numerator)
            else:
                if numerator == 1:
                    return r"$\frac{{\pi}}{{{}}}$".format(denominator)
                else:
                    return r"$\frac{{{}}}{{{}}}\pi$".format(numerator, denominator)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    # X축 눈금 라벨 위치 조정
    # `pad` 값을 음수로 설정하여 라벨 위치 조절 (이전 오류 발생 지점이었음)
    # 현재 Matplotlib 버전에서 이 부분이 문제가 된다면 다른 방법을 찾아야 합니다.
    ax.tick_params(axis='x', pad=-15,  # pad 값을 조정하여 라벨 위치 조절
                   labelbottom=True,      # 아래쪽 라벨 표시
                   bottom=False)          # X축 아래쪽의 작은 눈금 선 자체를 제거


    if function_type == "tan(x)":
        # 점근선 표시 (끊어진 선으로 표현)
        cos_val = np.cos(frequency * x + x_shift)
        
        asymptote_indices = np.where(np.isclose(cos_val, 0, atol=tolerance))[0]
        
        drawn_asymptotes = set()
        for i in asymptote_indices:
            asymptote_x = x[i] # 이 부분에서 x(i) -> x[i]로 수정되어야 합니다.
            if round(asymptote_x, 2) in drawn_asymptotes or not (x_min_plot <= asymptote_x <= x_max_plot):
                continue
            
            ax.plot([asymptote_x, asymptote_x], [-8, 8], color='red', linestyle='--', linewidth=1)
            drawn_asymptotes.add(round(asymptote_x, 2))

    st.pyplot(fig)

    st.subheader("설명")
    st.write("""
    이 앱은 스트림릿을 사용하여 삼각함수 그래프를 그립니다.
    왼쪽 사이드바에서 다음 파라미터들을 조정하여 그래프의 모양을 변경할 수 있습니다:

    * **함수 선택**: `sin(x)`, `cos(x)`, `tan(x)` 중 하나를 선택합니다.
    * **진폭 (A)**: 그래프의 높낮이를 조절합니다. (범위: 0 ~ 4)
    * **주파수 (B)**: 파동의 밀도를 조절합니다. 값이 클수록 파동이 더 조밀해집니다.
    * **X축 이동 (C)**: 그래프를 좌우로 이동시킵니다. 양수 값은 오른쪽으로 이동, 음수 값은 왼쪽으로 이동합니다.
    * **Y축 이동 (D)**: 그래프를 상하로 이동시킵니다.

    **일반적인 삼각함수 방정식:** $y = A \cdot \text{function}(B x + C) + D$
    """)

if __name__ == "__main__":
    main()
