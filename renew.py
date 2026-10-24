import os
import sys
from curl_cffi import requests

def run_auto_renew():
    glass_token = os.getenv("GLASS_TOKEN")
    if not glass_token:
        print("❌ 错误: 未能在环境变量中找到 GLASS_TOKEN！")
        sys.exit(1)

    url = "https://123.tsm.cc.cd/api/request_renewal"

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
        # 尝试带一个空的 json 体防止后端因 Content-Type 报错
        response = requests.post(
            url,
            headers=headers,
            json={}, 
            impersonate="chrome120",
            timeout=20
        )

        print(f"📡 HTTP 状态码: {response.status_code}")
        print(f"📄 接口返回内容: {response.text}")

        # 如果服务器返回 500，但你确认 Token 没问题，可以暂不让 Action 报错退出，
        # 或者等剩余天数小于 15 天（按钮出现时）再看它是否恢复 200。
        if response.status_code == 200:
            print("✅ 自动续期请求成功触发！")
        else:
            print("⚠️ 服务器返回了非 200 状态，请检查是否尚未到可续期时间。")

    except Exception as e:
        print(f"❌ 发送请求发生异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_auto_renew()
