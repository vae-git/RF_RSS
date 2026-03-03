import feedparser
from googletrans import Translator
import requests
import os

# 1. 配置期刊 RSS 列表 (已更新为稳定版链接)
RSS_FEEDS = [
    "https://ieeexplore.ieee.org/rss/TOC22.xml",   # T-MTT
    "https://ieeexplore.ieee.org/rss/TOC8.xml",    # T-AP
    "https://ieeexplore.ieee.org/rss/TOC7260.xml"  # MWTL
]

def translate_text(text):
    try:
        translator = Translator()
        # 尝试翻译标题
        return translator.translate(text, dest='zh-cn').text
    except:
        return text # 翻译失败则返回原文

def send_wechat(content):
    # 这里从 GitHub Secrets 获取你填写的 SERVER_CHAN_KEY
    send_key = os.environ.get('SERVER_CHAN_KEY')
    if not send_key:
        print("错误：未设置 SERVER_CHAN_KEY")
        return
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        "title": "📡 射频期刊每日更新",
        "desp": content
    }
    requests.post(url, data=data)

def main():
    combined_msg = ""
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        if feed.entries:
            # 获取最新的一篇文章
            entry = feed.entries[0]
            title_cn = translate_text(entry.title)
            combined_msg += f"### {feed.feed.get('title', '未知期刊')}\n"
            combined_msg += f"- **标题**: {title_cn}\n"
            combined_msg += f"- [查看原文]({entry.link})\n\n---\n"
    
    if combined_msg:
        # ⚠️ 注意：这里调用的名字必须和上面定义的 def send_wechat 一致
        send_wechat(combined_msg)
    else:
        print("未抓取到新内容")

if __name__ == "__main__":
    main()
