# SillyTavern 酒馆 · 傻瓜式世界书生成器

`sillytavern` `酒馆` `傻瓜式世界书生成器` `世界书` `World Info` `Worldbook` `ST世界书` `角色卡配套` `好感度触发`

> Easy SillyTavern World Info / Worldbook JSON maker · **Chinese & English UI**  
> 不用手写 JSON，分步填表 → 一键导出可导入酒馆的世界书。

---

## 这是什么？

这是一个 **Windows 桌面小工具**，帮你快速做出 **SillyTavern（酒馆）世界书 JSON**：

1. 写 **世界观**
2. 填 **角色**（名字、年龄、身材、外貌、服装、背景……）
3. 设 **条件触发**（好感度到多少触发什么；捡到什么物品触发什么）
4. **导出** `entries` 格式世界书，直接在 SillyTavern → World Info 导入

适合：不会写世界书 JSON、想可视化管理设定、要中英界面切换的用户。

---

## 截图级流程（怎么用）

### 方式 A：双击启动（推荐）

1. 安装 [Python 3.10+](https://www.python.org/downloads/)（勾选 Add to PATH）
2. 下载本仓库，解压
3. 双击 **`启动.bat`**（或 `Start.bat`）
4. 首次会自动 `pip install` 依赖，然后弹出窗口

### 方式 B：命令行

```bat
cd 傻瓜式sillytavern世界书生成器(中英双语)
pip install -r requirements.txt
python app.py
```

### 界面四步

| 步骤 | 中文 | English | 做什么 |
|------|------|---------|--------|
| 1 | 世界观 | Lore | 书名、关键词、设定正文；可勾选常驻 |
| 2 | 角色 | Cast | 左侧增删角色，右侧填档案；别名→关键词 |
| 3 | 触发 | Triggers | 好感度档位 / 捡到物品 / 自定义条件 |
| 4 | 导出 | Export | 预览 JSON → 导出世界书 或 保存工程草稿 |

右上角 **中 / EN** 可随时切换语言。顶部彩色步骤条可点击跳转。

### 导入 SillyTavern（酒馆）

1. 打开 SillyTavern
2. 进入 **世界书 / World Info**
3. **导入** 本工具导出的 `.json` 文件
4. 绑定到角色卡或全局启用

导出结构与酒馆世界书一致：

```json
{
  "entries": {
    "0": { "uid": 0, "comment": "...", "content": "...", "key": [], "constant": true, ... },
    "1": { ... }
  }
}
```

### 工程草稿

可 **保存工程草稿**（`.wbb.json`），下次用「打开」继续编辑。  
也可尽量打开已有世界书 JSON 回填（非本工具生成的文件为尽力解析）。

---

## 条件触发说明（重点）

### 好感度

- 指定角色名  
- 设置多档：例如 `≥20` / `≥50` / `≥80` 各写触发效果  
- 导出会生成世界书条目 + 一条常驻「好感度系统总则」

### 捡到物品

- 物品名（如某收集品）  
- 谁捡到：任何人 / 用户 / 角色 / 指定角色  
- 效果：触发什么剧情或状态

### 自定义

任意「条件 → 效果」文本。

---

## 打包成 EXE（可选）

```bat
build_exe.bat
```

生成：`dist\SillyTavernWorldbookMaker.exe`  
（打包前请先关掉正在运行的生成器窗口）

---

## 项目结构

```
├── app.py              # 主程序入口
├── 启动.bat / Start.bat
├── build_exe.bat
├── requirements.txt
├── i18n.py             # 中英文案
├── theme.py / ui_kit.py
├── core/               # 数据模型与 ST JSON 导出
└── ui/                 # 各步骤界面
```

---

## 依赖

- Python 3.10+
- `customtkinter`
- （打包）`pyinstaller`

```bat
pip install -r requirements.txt
```

---

## FAQ

**Q: 和角色卡有什么关系？**  
A: 本工具只做 **世界书 JSON**。角色卡请另做或用酒馆自带编辑器；世界书可绑定到角色卡使用。

**Q: 为什么没有「搜打撤 / 沉浸锁」预设？**  
A: 已刻意做成通用工具，不绑定某一款游戏模板；需要的规则请自己写在世界观或自定义触发里。

**Q: 导出后酒馆不触发？**  
A: 检查条目关键词、是否常驻、扫描深度；好感/拾取条目要在对话里出现相关关键词才会注入。

**Q: Mac / Linux？**  
A: 核心是 Python + CustomTkinter，理论上可运行；当前脚本与说明以 Windows 为主。

---

## License

MIT — 可自由使用、修改、分发。欢迎 Star / Issue / PR。

---

## Search / SEO

SillyTavern · 酒馆 · 傻瓜式世界书生成器 · ST 世界书 · World Info 可视化编辑 · 好感度世界书 · 中英双语世界书工具
