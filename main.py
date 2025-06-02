import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
    st.set_page_config(layout="wide")
    st.title("삼각함수 그래프 플로터")
    st.write("다양한 삼각함수 그래프를 동시에 그려보세요!")

    # 사이드바 입력 설정
    st.sidebar.header("그래프 설정")

    # 함수 선택 제거 (모든 함수를 동시에 표시)
    # function_type = st.sidebar.radio(...) 이 부분 삭제

    st.sidebar.subheader("공통 파라미터")

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

    st.subheader("그래프")
    # st.markdown(f"**현재 함수:** {formula}") # 단일 함수 표시 제거

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))

    # 사인 함수 (빨간색)
    y_sin = amplitude * np.sin(frequency * x + x_shift) + y_shift
    formula_sin = f"$y = {amplitude:.2f} \\sin({frequency:.2f}x + {x_shift:.2f}) + {y_shift:.2f}$"
    ax.plot(x, y_sin, color='red', label=formula_sin)

    # 코사인 함수 (파란색)
    y_cos = amplitude * np.cos(frequency * x + x_shift) + y_shift
    formula_cos = f"$y = {amplitude:.2f} \\cos({frequency:.2f}x + {x_shift:.2f}) + {y_shift:.2f}$"
    ax.plot(x, y_cos, color='blue', label=formula_cos)

    # 탄젠트 함수 (초록색)
    angle_tan = frequency * x + x_shift
    y_tan = amplitude * np.tan(angle_tan) + y_shift
    formula_tan = f"$y = {amplitude:.2f} \\tan({frequency:.2f}x + {x_shift:.2f}) + {y_shift:.2f}$"
    
    # 탄젠트 함수 점근선 처리 (y_masked를 사용)
    tolerance = 0.1
    y_tan_masked = np.ma.masked_where(np.abs(np.cos(angle_tan)) < tolerance, y_tan)
    ax.plot(x, y_tan_masked.filled(np.nan), color='green', label=formula_tan) # 마스킹된 데이터 플롯

    ax.set_xlabel("X축")
    ax.set_ylabel("Y축")
    ax.set_title("삼각함수 그래프") # 타이틀 변경
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=1.5) # x축 (y=0에 표현)
    ax.axvline(0, color='black', linewidth=0.8) # y축
    ax.spines['top'].set_visible(False)    # 위쪽 테두리 제거
    ax.spines['right'].set_visible(False)  # 오른쪽 테두리 제거
    ax.set_ylim(-8, 8) # Y축 범위 -8~8로 변경
    ax.set_xlim(x_min_plot, x_max_plot) # X축 범위 설정

    # X축 눈금을 파이/4의 배수로 설정
    major_locator = ticker.MultipleLocator(np.pi / 4)
    ax.xaxis.set_major_locator(major_locator)

    # 눈금 라벨 포맷터 정의
    def format_func(value, tick_pos):
        if value == 0:
            return "0"
        
        num = value / np.pi
        
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
    ax.tick_params(axis='x', which='both', bottom=False, labelbottom=True)

    # 텍스트 라벨 객체 가져오기
    tick_labels = ax.get_xticklabels()

    # 라벨의 y 위치를 데이터 좌표계 기준으로 조정 (y=0 바로 아래로)
    # y=0 데이터 포인트의 Axes 좌표를 계산합니다.
    y_position_in_data = 0 # y=0 라인 자체
    # 라벨 텍스트의 상단이 y=0에 닿도록 하려면, 라벨의 y 위치를 y=0에서 약간 아래로 설정해야 합니다.
    # 이 오프셋 값은 폰트 크기와 스타일에 따라 조정이 필요할 수 있습니다.
    # 텍스트 높이의 대략 절반만큼 아래로 내리면 중앙 정렬 상태에서 상단이 Y=0에 가까워집니다.
    # 좀 더 견고한 방법은 `ax.transData`와 `ax.transAxes`를 이용한 변환이지만,
    # 여기서는 간단히 데이터 좌표계에서 음수 오프셋을 줍니다.
    
    # 이 값은 라벨의 폰트 크기에 따라 조정이 필요합니다.
    # 경험상 0.5 ~ 1.0 정도의 음수 값이 적절할 수 있습니다.
    label_y_offset_from_zero = -0.5 # Y=0 데이터 포인트에서 아래로 이동할 오프셋
                                     # (조절하면서 가장 적절한 값을 찾으세요)

    for label in tick_labels:
        x_val = label.get_position()[0] # 원래 x 위치는 유지
        label.set_position((x_val, y_position_in_data + label_y_offset_from_zero))
        label.set_verticalalignment('top') # 텍스트의 상단이 지정된 y 위치에 닿도록

    # 탄젠트 함수 점근선 표시
    # 이 부분은 function_type 조건문 밖에 있어야 모든 함수에서 점근선이 표시됨
    # 하지만 탄젠트만 점근선이 있으므로 탄젠트 그래프 플롯 이후에 배치
    if True: # 탄젠트가 항상 그려지므로 True
        cos_val = np.cos(frequency * x + x_shift)
        asymptote_indices = np.where(np.isclose(cos_val, 0, atol=tolerance))[0]
        
        drawn_asymptotes = set()
        for i in asymptote_indices:
            asymptote_x = x[i]
            if round(asymptote_x, 2) in drawn_asymptotes or not (x_min_plot <= asymptote_x <= x_max_plot):
                continue
            
            ax.plot([asymptote_x, asymptote_x], [-8, 8], color='green', linestyle='--', linewidth=1, alpha=0.7) # 탄젠트와 같은 색상
            drawn_asymptotes.add(round(asymptote_x, 2))

    # 범례 표시
    ax.legend(loc='upper right', frameon=True, fontsize='medium') # 범례 추가

    st.pyplot(fig)

    st.subheader("설명")
    st.write("""
    이 앱은 스트림릿을 사용하여 삼각함수 그래프를 동시에 그립니다.
    왼쪽 사이드바에서 다음 파라미터들을 조정하여 그래프의 모양을 변경할 수 있습니다:

    * **진폭 (A)**: 그래프의 높낮이를 조절합니다. (범위: 0 ~ 4)
    * **주파수 (B)**: 파동의 밀도를 조절합니다. 값이 클수록 파동이 더 조밀해집니다.
    * **X축 이동 (C)**: 그래프를 좌우로 이동시킵니다. 양수 값은 오른쪽으로 이동, 음수 값은 왼쪽으로 이동합니다.
    * **Y축 이동 (D)**: 그래프를 상하로 이동시킵니다.

    **일반적인 삼각함수 방정식:** $y = A \cdot \text{function}(B x + C) + D$
    """)

if __name__ == "__main__":
    main()
