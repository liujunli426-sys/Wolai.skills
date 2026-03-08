# wolai.skill

连接 Wolai API 的技能，支持读取页面、创建页面、写入内容、操作数据库。

## 能做什么

- ✅ 自动同步笔记到 Wolai
- ✅ 从 Wolai 读取知识库信息
- ✅ 创建新页面/数据库条目
- ✅ 操作块结构（文本、标题、子页面）

## 安装

```bash
npx skills add openclaw-contrib/wolai.skill@v1.0.0 -g
```

或直接：

```bash
npx skills add https://github.com/openclaw-contrib/wolai.skill -g
```

## 配置

1. 在 [wolai 官网](https://www.wolai.com) 创建应用（头像 → 个人设置 → 应用设置）
2. 复制 AppId 和 AppSecret
3. 在 `config.json` 中填入：

```json
{
  "appId": "YOUR_APP_ID",
  "appSecret": "YOUR_APP_SECRET"
}
```

## 使用示例

```bash
# 创建新页面
python wolai_api.py create_page <parent_id> <title>

# 添加文本
python wolai_api.py add_text <page_id> <内容>

# 添加标题
python wolai_api.py add_heading <page_id> <标题> [level]

# 诊断
python wolai_api.py test_config
```

## 参考资料

- [Wolai 官方文档](https://www.wolai.com/wolai/7FB9PLeqZ1ni9FfD11WuUi)
- [Wolai API 文档](https://wolai.apifox.cn/)
