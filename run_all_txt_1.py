import glob
import os
import matplotlib.pyplot as plt
import pandas as pd

# 1. 현재 작업 중인 폴더의 이름을 자동으로 가져오기
current_folder_name = os.path.basename(os.getcwd())

# 2. '현재폴더이름_raman_graph'로 새 폴더 만들기 (예: 20260827_raman_graph)
output_dir = f"{current_folder_name}_raman_graph"
os.makedirs(output_dir, exist_ok=True)

txt_files = sorted(glob.glob("*.txt"))

print(f"'{output_dir}' 폴더에 총 {len(txt_files)}개의 그래프 저장을 시작할게...\n")

for file_path in txt_files:
    file_name = os.path.basename(file_path)
    title_name = os.path.splitext(file_name)[0]

    try:
        # comment="#"를 사용해 첫 줄(헤더 설명)을 무시하고 숫자 데이터만 읽기
        df = pd.read_csv(file_path, sep=r"\s+", comment="#", header=None)

        # 데이터가 4열 이상인 경우 (3열: Wave, 4열: Intensity)
        if df.shape[1] >= 4:
            wave = pd.to_numeric(df.iloc[:, 2], errors="coerce")
            intensity = pd.to_numeric(df.iloc[:, 3], errors="coerce")
        else:
            # 2열짜리 파일이 섞여 있을 경우를 대비
            wave = pd.to_numeric(df.iloc[:, 0], errors="coerce")
            intensity = pd.to_numeric(df.iloc[:, 1], errors="coerce")

        valid = (~wave.isna()) & (~intensity.isna())
        wave = wave[valid]
        intensity = intensity[valid]

        # 여러 스펙트럼이 합쳐진 맵핑 파일의 선 꼬임 방지: 파수(Wave)별 평균 내기
        plot_df = pd.DataFrame({'Wave': wave, 'Intensity': intensity})
        plot_df = plot_df.groupby('Wave').mean().reset_index()
        
        # 파수를 기준으로 오름차순 정렬해서 선이 자연스럽게 이어지게 설정
        plot_df = plot_df.sort_values('Wave')

        x = plot_df['Wave']
        y = plot_df['Intensity']

        # --- 예시 이미지 스타일 적용 ---
        fig, ax = plt.subplots(figsize=(10, 5.8), facecolor="white")
        ax.plot(x, y, color="#0e5f76", linewidth=1.2)
        
        ax.set_title(title_name, fontsize=14, pad=18, color="#333333", fontweight="normal")
        ax.set_xlim(x.min(), x.max())
        ax.grid(True, which="both", color="#e0e0e0", linestyle="-", linewidth=0.8)
        
        for spine in ax.spines.values():
            spine.set_color("#cccccc")
            spine.set_linewidth(1.0)
        ax.tick_params(colors="#555555", labelsize=10, length=4)

        # 이미지 저장
        save_path = os.path.join(output_dir, f"{title_name}.png")
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close(fig)

        print(f"✓ 저장 완료: {title_name}.png")

    except Exception as e:
        print(f"✗ 오류 발생 ({file_name}): {e}")

print(f"\n모든 작업 끝! '{output_dir}' 폴더 확인해봐 😎")