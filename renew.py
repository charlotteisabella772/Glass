import os
import sys
from curl_cffi import requests

def run_auto_renew():
    glass_token = os.getenv("GLASS_TOKEN")
    if not glass_token:
        print("❌ 错误: 未能在环境变量中找到 GLASS_TOKEN，请检查 Secrets 配置！")
        sys.exit(1)

    url = "https://123.tsm.cc.cd/api/request_renewal"

    # 全方位兼容各种后端可能读取 Token 的位置
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "authorization": f"Bearer {glass_token}",  # 兼容常见的 Bearer Token 格式
        "token": glass_token,                      # 兼容常见的自定义 token 标头
        "glass-token": glass_token,                # 兼容以键名命名的标头
        "cookie": f"glass_token={glass_token}",    # 保留 Cookie 兼容
        "origin": "https://123.tsm.cc.cd",
        "referer": "https://123.tsm.cc.cd/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 某些面板会将 token 作为参数直接放在 POST 的 JSON 请求体中
    payload = {
        "glass_token": glass_token
    }

    try:
        print("🚀 开始向接口发送续期请求（全兼容模式）...")
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
            print("⚠️ 服务器返回了非 200 状态。")

    except Exception as e:
        print(f"❌ 发送请求发生异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_auto_renew()
