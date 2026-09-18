# QUICKSTART.md — 开工指引（**先读这一份**）

> 这个仓库要把网课视频《心理学12》加工成一份好懂、好记的学习资料。
>
> **本文按顺序列出你要做的事。照着走就行。**

---

## 一、开工前自检（每次新会话都做，3 条命令）

```bash
# 1) 同步 —— 工作区不会自动拉新文件
git fetch origin && git merge origin/main

# 2) 确认在对的仓库里
git remote -v          # 必须指向本项目仓库，不是别的项目

# 3) 看根目录有哪些文件
ls -la                 # 应该看到 REQUIREMENTS.md / TASK.md / QUICKSTART.md 等
```

**如果第 2 条不对 → 立刻停止并汇报**（说明工作区绑错仓库了）。
**如果第 3 条看不到 `REQUIREMENTS.md` → 说明没同步成功**，重试第 1 条。

首次还要装环境（**只做一次**）：

```bash
bash setup.sh && source /etc/profile.d/pipeline.sh
```

装完 `$PY_OCR` 是带 Pillow / OCR 依赖的 Python。
**不装会在处理图片时报 `ModuleNotFoundError: No module named 'PIL'`。**

---

## 二、任务分三个阶段

### 阶段 0️⃣ · 清点全部文字素材（**先做，几分钟**）

**作业书：`TASK_READ_ALL_TEXT.md`** ｜ **产出：`out/STAGE0_INVENTORY.md`**

把仓库里**所有文字类文件**读一遍并汇报：`out/transcript.txt`、
`out/slides_unique.txt`、`out/ocr_all.jsonl`、`out/slides_index.md/.json`、
`out/slides/manifest.md`、`out/uniq_meta.json`、`out/asr_raw.jsonl`、
`out/幻灯片总览_高清版.html`（**先剥离 base64 再读**），
以及根目录全部 `.md` 和 `scripts/` 里的 14 个文件。

**目的**：先知道手里有什么，再动手。

---

### 阶段 1️⃣ · 把画面「看」成文字

> ## 📌 已选定路线：**幻灯片路线（102 张）**
>
> **作业书：`TASK_READ_BATCH.md`** ｜ **产出：`out/slides_vision.md`**
>
> 102 张 ÷ 每批 30~40 张 = **约 3~4 批**，预计 **1 小时左右**。

**为什么改用这条路线**：全帧路线（691 帧）每帧都要单独注入一张图片，
**102 次 vs 691 次 = 省约 85% 的 token**。而 **102 张已经覆盖所有内容不同的画面**
（102 张是从 691 帧里归并出来的唯一幻灯片）。

**为什么要做**：`out/slides_unique.txt` 的 OCR **抓不到**手写批注、颜色高亮、
树状/表格/箭头结构、插图 —— 而这些恰恰是老师解题的关键。

**怎么做**：解压 `out/frames/slides_102.zip`，用 **`functions.shell` 的 `image_path`**
参数逐张读（**一次一张**），写入 `out/slides_vision.md`。

> ⚠️ **必须用 `functions.shell` + `image_path`。**
> ❌ 不要用 `functions.display_multimedia` —— 它只返回链接，不提供视觉输入。
> 详见 **`HOW_TO_READ_IMAGES.md`**。

**批次范围由用户在对话里告诉你**，例如"本次范围：S001~S040"。
**断点续跑，读到哪算哪，不会浪费。**

<details>
<summary>已完成的补充记录：<code>out/frames_vision.md</code>（691 帧路线的前 40 帧）</summary>

在切换到本路线之前，已经用「全帧路线」读过 **F001～F040**（对应视频 00:27 ~ 11:51），
产出 `out/frames_vision.md`（22.6 KB）。

**这份记录保留**，作为开头的补充细节（它比 102 张路线更细，连讲师小窗动作、
水印变化都记了）。**不需要继续读后面的 651 帧** —— 那部分用 102 张路线覆盖即可。
</details>

<details>
<summary>备选：全帧路线（691 帧，太贵，已弃用）—— 点开查看原因</summary>

作业书 `TASK_READ_FRAMES.md`，产出 `out/frames_vision.md`。

**实测：40 帧就消耗了大量 token。** 原因是**每一帧都要单独注入一张图片**，
691 帧 = 691 次图片注入，成本约是 102 张路线的 **6.8 倍**。

**已弃用。** 除非将来有特殊需要，不再使用这条路线。
</details>

---

### 阶段 2️⃣ · 做学习资料

**作业书：`REQUIREMENTS.md`（最高优先级）+ `TASK.md`**

**输入素材**：

| 文件 | 内容 |
|---|---|
| `out/transcript.txt` | 老师讲的每一句话（45,541 字）← **真相源** |
| `out/slides_unique.txt` | 102 张幻灯片的 OCR |
| `out/ocr_all.jsonl` | 691 帧逐帧 OCR |
| `out/slides_index.md` | 691 行「画面 ↔ 讲解」对照表 |
| **`out/slides_vision.md` / `out/frames_vision.md`** | **逐张读图记录（阶段 1 的产出，补 OCR 之缺）** |
| `out/OCR_GAPS.md` | OCR 漏掉信息的汇总（阶段 1 末尾产出） |

**验收标准**：见 `REQUIREMENTS.md` 第三节（六条：覆盖度 / 通俗度 / 记忆度 /
做题度 / 体验度 / 形式）。**方法由你自己决定。**

---

## 三、文件导航

| 文件 | 作用 | 优先级 |
|---|---|---|
| **`REQUIREMENTS.md`** | 考生原始要求 + 验收标准 | ⭐ **最高** |
| **`QUICKSTART.md`** | 本文，开工指引 | ⭐ 先读 |
| `TASK.md` | 素材清单与读取方法 | 高 |
| `TASK_READ_BATCH.md` | 分批读图作业书 | 高 |
| `HOW_TO_READ_IMAGES.md` | 读图方法（工具、注意事项） | 高 |
| `CLAUDE.md` | 沙箱操作细节 | 中 |
| `BRIEF.md` | 制作规格**参考**（不是必须遵守） | 参考 |
| `TEST*.md` | 历史测试记录，**可忽略** | 忽略 |

---

## 四、常见坑（都是踩过的）

| 现象 | 原因 | 解决 |
|---|---|---|
| "仓库里没有 XXX 文件" | 工作区没同步 | `git fetch origin && git merge origin/main` |
| "仓库只有空的 README.md" | **工作区绑错仓库了** | 改 workspace 配置，选对仓库 |
| "我看不见图片" | **用错工具了** | 改用 `functions.shell` + `image_path` |
| `No module named 'PIL'` | 没装环境 | `bash setup.sh && source /etc/profile.d/pipeline.sh` |
| 读到一半上下文爆了 | 一批读太多 | 少读一点，断点续跑会自动接上 |

---

## 五、一句话

> **先自检 → 再分批读图 → 最后做资料。**
> **每次开工第一句永远是：`git fetch origin && git merge origin/main`。**
