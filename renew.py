import os
import sys
from curl_cffi import requests

def run_auto_renew():
    # 从环境变量中读取你在 GitHub Secrets 里配置的 glass_token
    glass_token = os.getenv("GLASS_TOKEN")
    if not glass_token:
        print("❌ 错误: 未能在环境变量中找到 GLASS_TOKEN，请检查 Secrets 配置！")
        sys.exit(1)

    url = "https://123.tsm.cc.cd/api/request_renewal"

    # 将 glass_token 包装进 Cookie 头部发送给后端接口
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "cookie": f"glass_token={glass_token}",
        "origin": "https://123.tsm.cc.cd",
        "referer": "https://123.tsm.cc.cd/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        print("🚀 开始向接口发送续期请求...")
        response = requests.post(
            url,
            headers=headers,
            impersonate="chrome120",
            timeout=20
        )

        print(f"📡 HTTP 状态码: {response.status_code}")
        print(f"📄 接口返回内容: {response.text}")

        if response.status_code == 200:
            print("✅ 自动续期请求成功触发！")
        else:
            print("❌ 请求返回非 200 状态，续期可能未成功，请检查 Token 是否失效。")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 发送请求发生异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_auto_renew()
