import feedparser
from googletrans import Translator
import requests
import os
import time

# 采用 IEEE 最稳固的 TOC 订阅链接
RSS_FEEDS = {
    "T-MTT": "https://ieeexplore.ieee.org/rss/TOC22.xml",
    "T-AP": "https://ieeexplore.ieee.org/rss/TOC8.xml",
    "MWTL": "https://ieeexplore.ieee.org/rss/TOC7260.xml",
    "JSSC": "https://ieeexplore.ieee.org/rss/TOC4.xml"
}

def translate_text(text):
    if not text: return ""
    try:
        # 强制使用特定版本的 Google 翻译库
        translator = Translator()
        result = translator.translate(text, dest='zh-cn')
        return result.text
    except Exception as e:
        print(f"翻译出错: {e}")
        return text  # 翻译失败则显示英文原文

def send_wechat(content):
    send_key = os.environ.get('SERVER_CHAN_KEY')
    if not send_key:
        print("错误：未设置 SERVER_CHAN_KEY")
        return
    
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        "title": "📡 射频期刊每日更新",
        "desp": content
    }
    res = requests.post(url, data=data)
    print(f"推送回执: {res.text}")

def main():
    combined_msg = "### 📚 射频领域最新论文 \n\n"
    has_update = False
    
    for name, url in RSS_FEEDS.items():
        try:
            print(f"正在抓取: {name}")
            # 增加 User-Agent 伪装，防止被 IEEE 拦截
            feed = feedparser.parse(url)
            
            if feed.entries:
                # 仅取当天最新的一篇，防止微信刷屏
                entry = feed.entries[0]
                title_cn = translate_text(entry.title)
                combined_msg += f"#### 【{name}】\n- **标题**: {title_cn}\n- [点击阅读原文]({entry.link})\n\n---\n"
                has_update = True
        except Exception as e:
            print(f"{name} 抓取失败: {e}")

    # 如果没有任何更新，也发一条通知确认脚本在跑（测试期建议开启）
    if not has_update:
        combined_msg += "今日目标期刊暂无内容更新。"
    
    send_wechat(combined_msg)

if __name__ == "__main__":
    main()
