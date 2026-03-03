import feedparser
from googletrans import Translator
import requests
import os

def send_wechat_debug(content):
    send_key = os.environ.get('SERVER_CHAN_KEY')
    print(f"DEBUG: 正在尝试使用的 Key 是: {send_key[:5]}******") # 仅打印前5位保护隐私
    
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        "title": "📡 射频机器人通道测试",
        "desp": content if content else "今日期刊无更新，这是一条通道测试消息。"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"DEBUG: Server酱返回结果: {response.text}")
    except Exception as e:
        print(f"DEBUG: 推送过程中发生网络错误: {e}")

def main():
    # 强制执行推送，不管有没有抓取到内容
    test_content = "### 联通性测试成功！\n如果您看到这条消息，说明微信通道已彻底打通。"
    send_wechat_debug(test_content)

if __name__ == "__main__":
    main()
