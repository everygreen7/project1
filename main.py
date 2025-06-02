import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

    # X축 라벨을 위한 빈 눈금 설정 (라벨 위치는 따로 조정)
    # 기존 tick_params 관련 오류 발생 부분을 제거하거나 기본값으로 둡니다.
    # 라벨을 수동으로 위치시키므로, 기본 tick_params는 최소한으로만 설정합니다.
    ax.tick_params(axis='x', which='both', bottom=False, labelbottom=True) # 아래쪽 눈금 숨기고 라벨은 유지

    # X축 눈금 위치와 라벨 가져오기
    # ax.get_xticks()는 숫자 값, ax.get_xticklabels()는 텍스트 객체
    ticks = ax.get_xticks()
    labels = [format_func(t, i) for i, t in enumerate(ticks)] # 라벨 포맷터 직접 적용

    # X축 눈금 라벨 위치 조정
    # 각 라벨 객체의 y 좌표를 변경합니다.
    # 이 부분은 그래프의 크기, 폰트 크기 등에 따라 조정이 필요할 수 있습니다.
    # 텍스트 위치를 y=0.0에 상대적으로 조정하기 위해 transform을 사용합니다.
    # ax.transAxes는 축의 좌표계를 의미하며, y=0.0은 축의 가장 아래를 나타냅니다.
    # `transform=ax.get_xaxis_transform()`은 데이터 좌표가 아닌 축의 좌표계를 사용하여 라벨 위치를 지정할 때 유용합니다.
    # 이 경우 `ax.xaxis.set_ticklabels(labels, y=y_position)` 형태로 직접 y 위치를 지정할 수 있습니다.
    
    # 1. 먼저 눈금 라벨을 설정합니다.
    ax.set_xticks(ticks) # 기존 눈금 위치 재설정
    ax.set_xticklabels(labels) # 포맷팅된 라벨 설정

    # 2. 각 라벨의 Y 위치를 개별적으로 조정합니다.
    # 이 값은 그래프의 Y축 범위에 따라 0.0 ~ 1.0 (축의 아래에서 위) 사이의 값입니다.
    # -0.05는 X축 (y=0) 바로 위가 아니라, 그래프의 가장 아래쪽에서 약간 위로 올라오는 위치입니다.
    # Y=0에 정확히 맞추려면, Y축 데이터 좌표로 변환해야 할 수 있습니다.
    # 더 좋은 방법은 `y=ax.transData.transform((0,0))[1]`을 사용하여 y=0의 화면 좌표를 얻는 것입니다.
    
    # 간단하게, `y` 인자를 사용하여 라벨의 수직 위치를 조정합니다.
    # 이 `y` 값은 0.0 (축 바닥) ~ 1.0 (축 상단) 사이의 비율입니다.
    # 0.05는 X축의 바닥에서 5% 정도 위에 표시됩니다.
    # 만약 Y=0에 정확히 맞추고 싶다면, `ax.transData.transform((0,0))`을 사용하여 데이터 좌표 0의 화면 좌표를 구해야 합니다.
    # 그러나 이것은 더 복잡해지므로, `pad` 대신 `y`를 사용한 상대적인 위치 조정으로 대체하겠습니다.
    
    # Matplotlib 3.8+에서 라벨의 Y 위치를 직접 조절하는 방법
    # `y` 인자는 Axes의 Y좌표(0:bottom, 1:top) 기준으로 라벨의 중심을 배치합니다.
    # y=0 라인에 라벨을 근접하게 배치하려면, 약간의 시행착오가 필요합니다.
    # 여기서 `0`은 Axes의 하단, `1`은 상단을 의미합니다.
    # 0에 가까운 작은 양수 값 (예: -0.01)을 사용하면 됩니다.
    # ax.tick_params(axis='x', bottom=False)는 그대로 두고,
    # ax.set_xticklabels(...)에서 y 위치를 조정하는 방법을 사용합니다.

    # 텍스트 라벨 객체 가져오기
    xticks_labels = ax.get_xticklabels()

    # 라벨의 y 위치를 조정합니다.
    # 이 값을 조절하여 y=0 선에 얼마나 가깝게 붙일지 결정합니다.
    # (예: 0.0은 축의 가장 아래, 0.5는 축의 중앙, 1.0은 축의 가장 위)
    # y=0 선 근처로 옮기려면, 이 값을 -0.01 ~ 0.03 사이에서 조정해 보세요.
    # 0.01은 X축 라벨이 X축 라인보다 약간 위에 오는 경우입니다.
    # 현재 Y축 범위가 -8~8이므로, X축 라인 (y=0)의 Axes 좌표는 0.5입니다.
    # 그래서 라벨을 0.5 근처로 옮겨야 합니다.
    # `va='center'`를 추가하여 텍스트의 수직 정렬을 중심으로 맞춥니다.

    # 텍스트 라벨을 Y=0 근처로 이동
    # 이 방법은 Matplotlib의 특정 버전에서 호환되지 않을 수 있는 기존 `pad` 문제를 회피합니다.
    # 라벨의 y 위치를 직접 설정합니다.
    # 0.5는 현재 Axes의 Y축에서 y=0에 해당하는 위치 (range -8 to 8)
    # 오프셋 값 (예: 0.02)을 빼거나 더해서 미세 조정합니다.
    # 0.02 (Axes의 상대적인 높이)는 텍스트가 Y=0 라인보다 약간 위에 위치하도록 합니다.
    # 폰트 크기에 따라 이 값은 조정이 필요할 수 있습니다.
    
    # 1. 눈금 라벨의 텍스트 객체를 가져옵니다.
    tick_labels = ax.get_xticklabels()
    
    # 2. 각 텍스트 객체의 위치를 조정합니다.
    # y=0 데이터 포인트의 Axes 좌표를 계산합니다.
    # (data_y - ax_ylim_min) / (ax_ylim_max - ax_ylim_min)
    # (0 - (-8)) / (8 - (-8)) = 8 / 16 = 0.5
    y_position_in_axes = (0 - ax.get_ylim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
    
    # 라벨을 y=0 라인보다 약간 위로 올리려면 y_position_in_axes에 작은 값을 더합니다.
    # 이 값은 라벨의 폰트 크기, 패딩에 따라 달라질 수 있습니다.
    # 0.02는 Axes 높이의 2%를 의미합니다.
    label_y_offset = 0.02 # Y축 라벨을 위로 올릴 오프셋 (Axes 단위)
    
    for label in tick_labels:
        # 텍스트의 y 위치를 설정하고, 수직 정렬을 가운데로 맞춥니다.
        # transform=ax.transAxes는 y_position_in_axes가 Axes 좌표계임을 명시합니다.
        # 기존 텍스트 객체의 위치를 유지하고, y 위치만 조정합니다.
        x_val = label.get_position()[0] # 원래 x 위치는 유지
        label.set_position((x_val, y_position_in_axes + label_y_offset))
        label.set_verticalalignment('center') # 수직 정렬

    # X축의 눈금(tick marks) 자체를 숨깁니다.
    # 라벨은 `labelbottom=True`로 인해 여전히 표시됩니다.
    ax.tick_params(axis='x', which='both', bottom=False)
    
    if function_type == "tan(x)":
        # 점근선 표시 (끊어진 선으로 표현)
        cos_val = np.cos(frequency * x + x_shift)
        
        asymptote_indices = np.where(np.isclose(cos_val, 0, atol=tolerance))[0]
        
        drawn_asymptotes = set()
        for i in asymptote_indices:
            asymptote_x = x[i]
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
