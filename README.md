# Wolai.skills

Wolai API Skill for OpenClaw - Read pages, create pages, write content, operate databases.

## Features

- ✅ Sync notes to Wolai automatically
- ✅ Read knowledge base from Wolai
- ✅ Create new pages/database entries
- ✅ Operate blocks (text, heading, subpages)

## Installation

```bash
npx skills add https://github.com/liujunli426-sys/Wolai.skills -g
```

## Configuration

1. Create an app in [wolai website](https://www.wolai.com)
2. Copy AppId and AppSecret
3. Fill in `config.json`:

```json
{
  "appId": "YOUR_APP_ID",
  "appSecret": "YOUR_APP_SECRET"
}
```

## Usage

```bash
python wolai_api.py create_page <parent_id> <title>
python wolai_api.py add_text <page_id> <content>
python wolai_api.py add_heading <page_id> <title> [level]
python wolai_api.py test_config
```

## References

- [Wolai Official Docs](https://www.wolai.com/wolai/7FB9PLeqZ1ni9FfD11WuUi)
- [Wolai API Docs](https://wolai.apifox.cn/)
