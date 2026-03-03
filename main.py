import feedparser
from googletrans import Translator
import requests
import os

# 配置期刊 RSS 列表
RSS_FEEDS = [
    "https://ieeexplore.ieee.org/rss/TOC22.xml",   # T-MTT
    "https://ieeexplore.ieee.org/rss/TOC8.xml",    # T-AP
    "https://ieeexplore.ieee.org/rss/TOC7260.xml"  # MWTL
]

def translate_text(text):
    try:
        translator = Translator()
        return translator.translate(text, dest='zh-cn').text
    except:
        return text # 翻译失败返回原文

def send_wechat(content):
    # 将 PUSHDEER_KEY 替换为你的 Server酱 SendKey
    send_key = os.environ.get('SERVER_CHAN_KEY')
    # Server酱的接口地址
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        "title": "射频期刊每日更新",
        "desp": content
    }
    requests.post(url, data=data)
def main():
    combined_msg = "### 📡 射频期刊每日更新 \n\n"
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        # 仅取最新的一条进行推送，避免刷屏
        if feed.entries:
            entry = feed.entries[0]
            title_cn = translate_text(entry.title)
            combined_msg += f"**【{feed.feed.title}】**\n- **标题**: {title_cn}\n- [查看原文]({entry.link})\n\n---\n"
    
    send_pushdeer(combined_msg)

if __name__ == "__main__":
    main()
