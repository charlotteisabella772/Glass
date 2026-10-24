import os
import sys
from curl_cffi import requests

def run_auto_renew():
    glass_token = os.getenv("GLASS_TOKEN")
    if not glass_token:
        print("❌ 错误: 未能在环境变量中找到 GLASS_TOKEN，请检查 Secrets 配置！")
        sys.exit(1)

    # 自动从 token 中截取出用户名（例如 jiedian0809:mvgl0ka0... 会被拆出 jiedian0809）
    try:
        username = glass_token.split(":")[0]
    except Exception:
        username = ""

    url = "https://123.tsm.cc.cd/api/request_renewal"

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://123.tsm.cc.cd",
        "referer": "https://123.tsm.cc.cd/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 严格匹配抓包显示的 JSON 载荷格式
    payload = {
        "token": glass_token,
        "username": username
    }

    try:
        print(f"🚀 正在为用户 [{username}] 发送续期请求...")
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            impersonate="chrome120",
            timeout=20
        )

        print(f"📡 HTTP 状态码: {response.status_code}")
        print(f"📄 接口返回内容: {response.text}")

        if response.status_code == 200:
            print("✅ 自动续期请求成功触发！")
        else:
            print("⚠️ 服务器返回了非 200 状态（如果未到可续期时间，服务器可能会拒绝）。")
            # 视情况决定是否 exit(1)，如果没到期报错可以先不让 workflow 失败

    except Exception as e:
        print(f"❌ 发送请求发生异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_auto_renew()
