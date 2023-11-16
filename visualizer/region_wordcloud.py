import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def init_plt():
    plt.style.use('seaborn')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False


def draw_word_cloud(tag_path: str, save_path: str):
    df = pd.read_csv(tag_path)
    tags_raw = df['标签'].values.tolist()
    tag_list = []
    for tag_raw in tags_raw:
        tag_list.extend(tag_raw.split(','))
    wc = WordCloud(
        scale=5,
        margin=0,
        background_color="black",
        max_words=1200,
        width=200,
        height=200,
        font_path=r'C:\Windows\Fonts\STSONG.TTF',
        random_state=800,
    )
    wc.generate_from_text(" ".join(tag_list))
    wc.to_file(save_path)


if __name__ == "__main__":
    init_plt()
    draw_word_cloud('result/crawl_result/region_tag/科技.csv', "result/visualize_result/region_tag/科技_词云图.png")