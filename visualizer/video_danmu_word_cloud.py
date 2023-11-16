import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def init_plt():
    plt.style.use('seaborn')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False


def draw_word_cloud(danmu_path: str, save_path: str):
    df = pd.read_csv(danmu_path)
    danmu_list = df['弹幕'].values.tolist()
    wc = WordCloud(
        scale=5,
        margin=0,
        background_color="black",
        max_words=1200,
        width=200,
        height=200,
        font_path=r'C:\Windows\Fonts\STSONG.TTF',
        random_state=800
    )
    wc.generate_from_text(" ".join(danmu_list))
    wc.to_file(save_path)


if __name__ == "__main__":
    init_plt()
    draw_word_cloud('result/crawl_result/video_danmu/弹幕.csv', "result/visualize_result/video_danmu/弹幕.png")