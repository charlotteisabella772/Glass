import os
import sys
from curl_cffi import requests

BASE = "https://123.tsm.cc.cd"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "origin": BASE,
    "referer": f"{BASE}/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def login(username: str, password: str) -> str:
    """调 POST /api/user_login 拿新 token，返回 token（格式 username:xxxx）"""
    url = f"{BASE}/api/user_login"
    payload = {"type": "login", "username": username, "password": password, "turnstileToken": None}
    resp = requests.post(url, headers=HEADERS, json=payload, impersonate="chrome120", timeout=20)
    print(f"📡 登录接口 HTTP 状态码: {resp.status_code}")
    print(f"📄 登录接口返回: {resp.text[:200]}")
    if resp.status_code != 200:
        print("❌ 登录失败，请检查用户名/密码")
        sys.exit(1)
    data = resp.json()
    if not data.get("success"):
        print(f"❌ 登录失败: {data.get('msg')}")
        sys.exit(1)
    token = data.get("token")
    if not token:
        print("❌ 登录返回里没有 token 字段")
        sys.exit(1)
    print(f"✅ 登录成功，用户: {data.get('username')}")
    return token

def run_auto_renew():
    # 优先用账号密码自动登录拿新 token；没配账号密码时，退回用旧的 GLASS_TOKEN
    username = os.getenv("GLASS_USERNAME") or ""
    password = os.getenv("GLASS_PASSWORD") or ""
    glass_token = os.getenv("GLASS_TOKEN") or ""

    if username and password:
        print("🔑 用账号密码自动登录拿新 token...")
        glass_token = login(username, password)
    elif not glass_token:
        print("❌ 错误: 未配置 GLASS_USERNAME/GLASS_PASSWORD，也没有 GLASS_TOKEN，请检查 Secrets 配置！")
        sys.exit(1)
    else:
        print("ℹ️ 未配置账号密码，沿用 Secrets 里的 GLASS_TOKEN（过期会报 401）")

    try:
        username = glass_token.split(":")[0]
    except Exception:
        username = ""

    url = f"{BASE}/api/request_renewal"
    payload = {"token": glass_token, "username": username}

    try:
        print(f"🚀 正在为用户 [{username}] 发送续期请求...")
        response = requests.post(url, headers=HEADERS, json=payload, impersonate="chrome120", timeout=20)
        print(f"📡 HTTP 状态码: {response.status_code}")
        print(f"📄 接口返回内容: {response.text}")
        if response.status_code == 200:
            print("✅ 自动续期请求成功触发！")
        elif response.status_code == 400:
            # 仅限到期前 15 天内申请续期：这是正常拒绝，不是脚本问题，不让 workflow 失败
            print("ℹ️ 未到可续期时间（到期前 15 天内才能续），这是正常情况。")
        elif response.status_code == 401:
            print("❌ token 已过期/无效，下次请确认账号密码登录能拿到新 token。")
            sys.exit(1)
        else:
            print("⚠️ 服务器返回了非 200 状态。")
    except Exception as e:
        print(f"❌ 发送请求发生异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_auto_renew()
