#!/usr/bin/env python3
"""
Wolai API 通用脚本
用于 OpenClaw 连接 Wolai，支持读取页面、创建页面、写入内容、操作数据库。

需要配置：
  config.json: { "appId": "xxx", "appSecret": "xxx" }
  放置位置：/home/admin/.openclaw/workspace/skills/wolai/config.json
"""

import json
import urllib.request
import sys
import os

# 配置路径
CONFIG_PATH = "/home/admin/.openclaw/workspace/skills/wolai/config.json"
API_BASE = "https://openapi.wolai.com/v1"

def load_config():
    """加载 config.json"""
    if not os.path.exists(CONFIG_PATH):
        print("❌ 错误：config.json 不存在")
        print(f"   请在 {CONFIG_PATH} 创建配置文件")
        sys.exit(1)
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_app_token():
    """获取 App Token（永久有效）"""
    config = load_config()
    req = urllib.request.Request(
        f"{API_BASE}/token",
        data=json.dumps({"appId": config["appId"], "appSecret": config["appSecret"]}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            print(f"[DEBUG] Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            if not isinstance(data, dict):
                print("[ERROR] API returned non-dict response")
                sys.exit(1)
            token = data.get("data", {}).get("app_token") if isinstance(data.get("data"), dict) else data.get("data") or data.get("app_token")
            if not token:
                print("[ERROR] Token not found in response")
                print("💡 检查点：")
                print("   1. AppId 是否正确（20-24位字母数字）")
                print("   2. AppSecret 是否包含特殊字符（如 `/`）")
                print("   3. 应用是否已激活（wolai 官网 → 个人设置 → 应用设置）")
                sys.exit(1)
            return token
    except urllib.error.HTTPError as e:
        print(f"❌ 认证失败 [{e.code}]: {e.read().decode()}")
        sys.exit(1)

def get_token_with_manual_config(app_id, app_secret):
    """支持手动传入凭证（用于测试）"""
    req = urllib.request.Request(
        f"{API_BASE}/token",
        data=json.dumps({"appId": app_id, "appSecret": app_secret}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            print(f"[DEBUG] Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            if not isinstance(data, dict):
                print("[ERROR] API returned non-dict response")
                sys.exit(1)
            token = data.get("data", {}).get("app_token") if isinstance(data.get("data"), dict) else data.get("data") or data.get("app_token")
            if not token:
                print("[ERROR] Token not found in response")
                print("💡 检查点：")
                print("   1. AppId 是否正确（20-24位字母数字）")
                print("   2. AppSecret 是否包含特殊字符（如 `/`）")
                print("   3. 应用是否已激活（wolai 官网 → 个人设置 → 应用设置）")
                sys.exit(1)
            return token
    except urllib.error.HTTPError as e:
        print(f"❌ 认证失败 [{e.code}]: {e.read().decode()}")
        sys.exit(1)

def wolai_request(method, path, data=None, token=None):
    """通用 Wolai API 请求"""
    if token is None:
        token = get_app_token()
    headers = {
        "Content-Type": "application/json",
        "authorization": token  # 注意：没有 Bearer 前缀！
    }
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        print(f"❌ API 错误 [{e.code}]: {body.get('message', 'Unknown error')}")
        print(f"   错误码: {body.get('code', 'N/A')}")
        print(f"   请求: {method} {path}")
        print(f"   数据: {json.dumps(data, ensure_ascii=False) if data else 'None'}")
        sys.exit(1)

# ========== 功能函数 ==========

def create_page(parent_id, title="新页面"):
    """创建新页面"""
    result = wolai_request("POST", "/blocks", {
        "parent_id": parent_id,
        "blocks": [{"type": "page", "content": title}]
    })
    # 兼容不同返回结构
    if isinstance(result, dict):
        if "data" in result:
            return result["data"][0] if isinstance(result["data"], list) else result["data"]
        if "id" in result:
            return result
    return result

def read_blocks(block_id):
    """读取块详情"""
    return wolai_request("GET", f"/blocks/{block_id}")

def get_children(block_id):
    """获取子节点列表"""
    return wolai_request("GET", f"/blocks/{block_id}/children")

def add_text(parent_id, content, level=None):
    """添加文本块"""
    block = {"type": "text", "content": content}
    if level:
        block["level"] = level
    result = wolai_request("POST", "/blocks", {
        "parent_id": parent_id,
        "blocks": [block]
    })
    if isinstance(result, dict):
        if "data" in result:
            return result["data"][0] if isinstance(result["data"], list) else result["data"]
        if "id" in result:
            return result
    return result

def add_heading(parent_id, title, level=1):
    """添加标题块"""
    result = wolai_request("POST", "/blocks", {
        "parent_id": parent_id,
        "blocks": [{"type": "heading", "level": level, "content": title}]
    })
    if isinstance(result, dict):
        if "data" in result:
            return result["data"][0] if isinstance(result["data"], list) else result["data"]
        if "id" in result:
            return result
    return result

def query_database(database_id):
    """查询数据库内容"""
    return wolai_request("GET", f"/databases/{database_id}")

def add_database_row(database_id, properties):
    """新增数据库行"""
    result = wolai_request("POST", f"/databases/{database_id}/rows", {"properties": properties})
    if isinstance(result, dict):
        if "data" in result:
            return result["data"]
        if "id" in result:
            return result
    return result

# ========== 命令行接口 ==========

def print_usage():
    print("用法:")
    print("  python wolai_api.py <command> [args]")
    print()
    print("命令:")
    print("  create_page <parent_id> [title]     创建新页面")
    print("  read_blocks <block_id>              读取块详情")
    print("  get_children <block_id>             获取子节点")
    print("  add_text <parent_id> <content>      添加文本块")
    print("  add_heading <parent_id> <title> [level]  添加标题")
    print("  query_database <database_id>        查询数据库")
    print("  add_row <database_id> <json>        新增数据库行")
    print()
    print("示例:")
    print("  python wolai_api.py create_page iAuov6BXtjt27LdBK8tVSy '新笔记'")
    print("  python wolai_api.py add_text iAuov6BXtjt27LdBK8tVSy '这是内容'")
    print()
    print("调试:")
    print("  python wolai_api.py test_config        测试当前配置")
    print("  python wolai_api.py debug_token <app_id> <app_secret>  手动测试凭证")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "create_page":
        if len(sys.argv) < 3:
            print("❌ 缺少 parent_id")
            sys.exit(1)
        parent_id = sys.argv[2]
        title = sys.argv[3] if len(sys.argv) > 3 else "新页面"
        result = create_page(parent_id, title)
        print(f"✅ 创建成功: {json.dumps(result, indent=2, ensure_ascii=False)}")

    elif cmd == "read_blocks":
        if len(sys.argv) < 3:
            print("❌ 缺少 block_id")
            sys.exit(1)
        result = read_blocks(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "get_children":
        if len(sys.argv) < 3:
            print("❌ 缺少 block_id")
            sys.exit(1)
        result = get_children(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "add_text":
        if len(sys.argv) < 4:
            print("❌ 缺少参数: parent_id content")
            sys.exit(1)
        result = add_text(sys.argv[2], sys.argv[3])
        print(f"✅ 添加成功: {result}")

    elif cmd == "add_heading":
        if len(sys.argv) < 4:
            print("❌ 缺少参数: parent_id title")
            sys.exit(1)
        level = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        result = add_heading(sys.argv[2], sys.argv[3], level)
        print(f"✅ 添加成功: {result}")

    elif cmd == "query_database":
        if len(sys.argv) < 3:
            print("❌ 缺少 database_id")
            sys.exit(1)
        result = query_database(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "add_row":
        if len(sys.argv) < 4:
            print("❌ 缺少参数: database_id json")
            sys.exit(1)
        props = json.loads(sys.argv[3])
        result = add_database_row(sys.argv[2], props)
        print(f"✅ 添加成功: {json.dumps(result, indent=2, ensure_ascii=False)}")

    elif cmd == "test_config":
        print("🧪 测试当前配置...")
        config = load_config()
        print(f"✅ 配置读取成功")
        print(f"   AppId: {config['appId'][:8]}...{config['appId'][-4:] if len(config['appId']) > 12 else config['appId']}")
        print(f"   AppSecret: {'*' * 8}{config['appSecret'][-8:] if len(config['appSecret']) > 8 else '*' * len(config['appSecret'])}")
        print()
        print("🔧 正在测试 Token API...")
        get_app_token()
        print("✅ Token 获取成功！")

    elif cmd == "debug_token":
        if len(sys.argv) < 4:
            print("❌ 缺少参数: app_id app_secret")
            sys.exit(1)
        app_id = sys.argv[2]
        app_secret = sys.argv[3]
        print(f"🧪 测试手动凭证...")
        print(f"   AppId: {app_id[:8]}...{app_id[-4:] if len(app_id) > 12 else app_id}")
        print(f"   AppSecret: {'*' * 8}{app_secret[-8:] if len(app_secret) > 8 else '*' * len(app_secret)}")
        token = get_token_with_manual_config(app_id, app_secret)
        print(f"✅ Token 获取成功: {token[:16]}...")

    else:
        print(f"❌ 未知命令: {cmd}")
        print_usage()
        sys.exit(1)
