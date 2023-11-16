import os
import pandas as pd
import matplotlib.pyplot as plt


def init_plt():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False


def calculate_play_cnt_for_csv(path: str):
    df = pd.read_csv(path)
    play_cnt = sum(df['播放数'].values.tolist())
    name = path.split(".")[0].split("\\")[-1]
    return name, play_cnt


def calculate_each_play_cnt_for_directory(path: str):
    play_cnts = []
    names = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            name, play_cnt = calculate_play_cnt_for_csv(os.path.join(path, file))
            play_cnts.append(play_cnt)
            names.append(name)
    return names, play_cnts


def show_play_cnt_for_each_region(directory: str, save_path: str):
    names, play_cnts = calculate_each_play_cnt_for_directory(directory)
    plt.figure(figsize=(20, 8))
    plt.pie(
        play_cnts,
        labels=names,
        autopct='%.2f%%',
    )
    plt.title("播放数-分布饼图")
    plt.savefig(save_path)


if __name__ == "__main__":
    init_plt()
    show_play_cnt_for_each_region("result/crawl_result/region_play", "result/visualize_result/region_play_cnt/播放数-饼图.png")