import requests
import os
import datetime

# --- 从 GitHub Secrets 安全读取配置 ---
NEWS_API_KEY = os.environ.get('c05aafa258ca4680b383f7334877b802')
PUSHPLUS_TOKEN = os.environ.get('2c84872cb1784b72b94007c97c47b775')
COUNTRY = 'br'
NEWS_COUNT = 20

def fetch_and_push():
    url = f"https://newsapi.org/v2/everything?q=Brazil OR Brasil&language=pt&sortBy=publishedAt&pageSize={NEWS_COUNT}&apiKey={NEWS_API_KEY}"
    # GitHub 服务器在海外，无需设置代理，直接请求
    response = requests.get(url, timeout=30)
    data = response.json()
    
    if data.get('status') == 'ok' and data.get('articles'):
        articles = data['articles']
        today = datetime.date.today().strftime("%m/%d")
        content = f"<h2>🇧🇷 巴西全领域新闻特刊 ({today})</h2><hr>"
        
        for i, art in enumerate(articles, 1):
            title = art.get('title', 'N/A')
            desc = art.get('description') or "（查看原文了解详情）"
            img = art.get('urlToImage')
            link = art.get('url')
            
            content += f"<div style='margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;'>"
            content += f"<h3>#{i} {title}</h3><p>{desc}</p>"
            if img:
                content += f'<img src="{img}" style="width:100%; border-radius:5px;" />'
            content += f'<p><a href="{link}">🔗 查看原文</a></p></div>'
            
        push_payload = {
            "token": PUSHPLUS_TOKEN,
            "title": f"🇧🇷 巴西 20 条全覆盖 {today}",
            "content": content,
            "template": "html"
        }
        requests.post("https://www.pushplus.plus/send", json=push_payload)
        print("✅ 推送成功")
    else:
        print("❌ 抓取失败，请检查配置")

if __name__ == "__main__":
    fetch_and_push()
