---
name: wolai
description: 连接 Wolai API 的技能，支持读取页面、创建页面、写入内容、操作数据库。使用场景：(1) 自动同步笔记到 Wolai (2) 从 Wolai 读取知识库信息 (3) 创建新页面/数据库条目 (4) 操作块结构（文本、标题、子页面）。需要配置 config.json（包含 appId 和 appSecret）。
---

# Wolai API 连接指南

## 快速开始

### 1. 配置凭证

在 `/home/admin/.openclaw/workspace/skills/wolai/config.json` 中填入你的应用凭证：

```json
{
  "appId": "YOUR_APP_ID",
  "appSecret": "YOUR_APP_SECRET"
}
```

👉 **如何获取凭证：**
1. 打开 [wolai 官网](https://www.wolai.com)
2. 点击左下角头像 → 个人设置
3. 进入「应用设置」→「创建和管理应用」
4. 点击「创建应用」，权限建议全选
5. 复制 AppId 和 AppSecret 填入 config.json

### 2. 获取页面 ID

打开 wolai 页面，复制 URL 最后 22 位作为 `parent_id`：
```
https://www.wolai.com/用户名/iAuov6BXtjt27LdBK8tVSy
                                 ↑ 22位ID
```

### 3. 使用示例

- **创建新页面**：`python wolai_api.py create_page <parent_id> <title>`
- **读取页面内容**：`python wolai_api.py read_blocks <block_id>`
- **写入文本块**：`python wolai_api.py add_text <parent_id> <内容>`
- **添加标题**：`python wolai_api.py add_heading <parent_id> <title> [level]`
- **查询数据库**：`python wolai_api.py query_database <database_id>`

## 🔍 诊断命令

```bash
# 测试当前配置
python wolai_api.py test_config

# 手动测试其他凭证
python wolai_api.py debug_token <app_id> <app_secret>
```

## API 认证

使用 `get_app_token()` 获取 permanent token（无需 Bearer 前缀）。

## 常用块类型

| 类型 | 说明 |
|------|------|
| `page` | 新页面（内容为标题） |
| `text` | 普通文本 |
| `heading` | 标题（需加 `level: 1~3`） |

## 错误码处理

- `17002` → `parent_id` 不存在，检查页面 ID
- `17011` → 不在应用所属空间，换自己的页面 ID
- `17005` → 块不存在或已删除
- `401` → Token 失效，重新运行 `get_app_token()`
- `400` → 请求格式错误（检查 JSON 结构）

## 参考资料

- 官方文档：https://www.wolai.com/wolai/7FB9PLeqZ1ni9FfD11WuUi
- API 文档（新）：https://wolai.apifox.cn/
- Python 示例：见 `references/wolai_api.py`
