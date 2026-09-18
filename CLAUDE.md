# CLAUDE.md — Hoplite 沙箱作业指导书

你是跑在 **Hoplite 沙箱（Linux / Docker Compose / Modal VM，4 vCPU · 8 GiB RAM · 无 GPU）** 里的 Agent。

> **本文件优先于 `scripts/SKILL.md`。**
> `scripts/SKILL.md` 是原作者在本机 Windows 上写的 SOP，里面所有
> `C:\Users\Jason\...`、`.exe`、`Scripts\python.exe`、**14 核**的性能数字
> —— 在本沙箱里**一律不成立，直接忽略**。流程和方法论照抄，路径和参数照本文件。

---

## ⚠️ 0. 开工前必做三件事（**别跳过**）

### 0.1 先同步代码 —— **工作区不会自动拉新文件**

```bash
git fetch origin && git merge origin/main
ls -la          # 确认要读的文件都在
```

**不先同步，会出现"文件不存在"** —— 因为工作区是你克隆时的快照，
而仓库里的文件可能在之后更新过。

### 0.2 确认自己在对的仓库里

```bash
git remote -v   # 应该指向本项目仓库，不是别的项目
```

**如果指向别的仓库，立刻停止并汇报** —— 说明工作区绑错仓库了。

### 0.3 装环境（首次才需要）

```bash
bash setup.sh && source /etc/profile.d/pipeline.sh
```

装完后 `$PY_ASR` / `$PY_OCR` 是带全部依赖的 Python（**含 Pillow、ffmpeg**）。
**没装环境就跑 OCR/图片处理会报 `ModuleNotFoundError: No module named 'PIL'`。**

---

## 🔴 读图片必须用对工具

**要「看到」图片内容，必须用 `functions.shell` 的 `image_path` 参数**：

```
functions.shell(command="ls slides/S001.jpg", image_path="/tmp/rt/slides/S001.jpg")
```

它会**把图片作为视觉附件返回** —— 你就能看到像素（颜色、手写、版式、插图）。

❌ **不要用 `functions.display_multimedia`** —— 它只返回 URL/Markdown 链接，
那是「发布给用户看」的工具，不是「读给模型看」的工具。用它会让你误以为"看不见图"。

**详细方法见 `HOW_TO_READ_IMAGES.md`。**

---

## 任务入口

具体要做什么，看根目录这几个文件（按优先级）：

1. **`REQUIREMENTS.md`** —— 考生原始要求 + 验收标准（**最高优先级**）
2. **`TASK.md`** —— 素材清单与读取方法
3. **`TASK_READ_BATCH.md`** —— 分批读图作业（102 张幻灯片）
4. **`HOW_TO_READ_IMAGES.md`** —— 读图方法
5. 本文件 —— 沙箱操作细节

---

## 1. 取视频（如需要）


```bash
bash fetch_video.sh          # 下载到 /work/video/，并打印绝对路径
```

下载用的是 Release 附件公网直链，**不需要 token**（`fetch_video.sh` 直接用 API 返回的
`browser_download_url`，中文文件名不需要自己拼 URL）。若中断，脚本带 `-C -` 断点续传，重跑即可。

**当前 release `v1` 里的东西**

| 附件名 | 内容 |
|---|---|
| `psychology-12.mov` | 2025年下教师编制课程 · 心理学12｜02:42:16｜552,772,816 字节（527 MiB）｜HEVC 1920×888 + AAC 44.1kHz stereo |

换视频时改 `TAG` 或 `ASSET` 环境变量，例如 `ASSET=psychology-13.mov bash fetch_video.sh`。

## 2. 跑流水线

```bash
source /etc/profile.d/pipeline.sh
mkdir -p /work/run1                       # 每次必须用全新的 workdir，不能复用
python -u scripts/run_pipeline.py \
    "$(cat /work/video/VIDEO_PATH)" /work/run1 \
    --out /work/out \
    --workers-asr 4 --workers-ocr 4 \
    --interval 2 --frame-width 1200
```

**参数说明（4 vCPU 特化，别照搬 SKILL.md 的 12）**
- `--workers-asr 4` / `--workers-ocr 4`：本机只有 4 vCPU，开再多只会抢 CPU。
- `--frame-width 1200`：一次抽到 1200 宽，去重和配图都够用，**省掉一遍全片重抽**。
- `--skip-frames`：只要文字稿时加，跳过抽帧/OCR，能省掉一半以上时间。
- `--minutes N`：只处理前 N 分钟（**已有本地验证记录，按需使用，不是必须**）。
- `--keep`：保留中间文件（默认会清理）。

## 3. 预期耗时（重要）

`scripts/SKILL.md` 里的产能数字是 **14 核**实测（2h48m 全片 26.7 分钟）。
本沙箱 **4 vCPU ≈ 3~4 倍耗时**，2.5 小时的视频预计：

| 阶段 | 14 核 | 4 vCPU | **1 vCPU（实测沙箱）** |
|---|---|---|---|
| 抽音频 | 快 | 1~2 分钟 | 2~4 分钟 |
| SenseVoice 转写 | 287 s | 15~20 分钟 | **约 55~70 分钟** |
| 抽帧 | 快 | 3~5 分钟 | 8~15 分钟 |
| 去重 | 31 s | 2~4 分钟 | 5~10 分钟 |
| 幻灯片 OCR | 834 s（440 帧） | 40~55 分钟 | **3 小时以上（会超时）** |
| 归并 | 快 | 1 分钟 | 2 分钟 |
| **合计** | 26.7 分钟 | 约 1.5~2 小时 | **4~5 小时** |

> ⚠️ **实测沙箱是 1 vCPU**（2026-09-16 探针结果，虽然面板写的是 4 vCPU）。
> **1 核下不要跑 OCR**，必然超时。策略：
> 1. 先 `git config --global --add safe.directory '*'` 之类的前置不管，**只跑 `--skip-frames`**，
>    约 1 小时出 `transcript.txt`，**立刻 commit 并 push**（见第 4 节）。
> 2. OCR / 抽帧 / 出手册**不在这个沙箱做** —— 交给别的方式（见 README「算力不足时」）。
> 3. 如果用户已把沙箱调到 4 vCPU 以上，才考虑跑完整流程。

## 4. 产出与回写

产物在 `/work/out/`：`transcript.txt`（带标点、术语纠正）、`slides_unique.txt`、
`ocr_all.jsonl`、`uniq_meta.json`。

**必须做**：把 `transcript.txt` 和 `slides_unique.txt` 复制到仓库根目录并 commit 回来：

```bash
cp /work/out/transcript.txt /work/out/slides_unique.txt <repo>/   # 几百 KB，随便放
git add -A && git commit -m "chore: <讲次名> 文字稿 + 幻灯片"
```

> ⚠️ **push 必须用 `-u origin HEAD`**，不能只写 `git push`：
> Hoplite 会在自动创建的分支（如 `hoplite/gortyn-xxxx`）上工作，**该分支没有 upstream**，
> 裸 `git push` 一定报 `fatal: The current branch ... has no upstream branch`（exit 128）。
>
> ```bash
> git push -u origin HEAD          # ✅ 正确
> git push                          # ❌ 必失败
> ```

> ⚠️ **绝不要把视频本体、frames/、audio16k.wav 提交进 git。**
> 它们会撑爆仓库并触发每晚重烘焙下载。`.gitignore` 已经挡住了，别手动 `git add -f`。

## 5. 之后写手册

拿到 `transcript.txt` + `slides_unique.txt` 后，按 `scripts/SKILL.md` 第 9 节
（撰写 HTML 手册 → 9b 学习化改造 → 9c 加「说人话 + 打个比方」）继续，
模板用 `scripts/skeleton.html`。这部分是纯文本工作，不占 CPU。

## 6. 已知坑（照做，别自己发挥）

- `ffmpeg -ss` 快进 seek 在这些 MOV 上**不可靠**，别用它截取时间点。
- 换视频重跑时**必须换新的 workdir**，否则脚本看到 `frames/` 非空会跳过抽帧，后面全基于残缺帧集。
- 清理几千个中间文件用 `scripts/recycle_purge.py`，别用 `rm -rf` / `shutil.rmtree`（会卡）。
- 模型下载走 **hf-mirror.com**（`https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/resolve/main`），
  modelscope 上没有这个仓库，别去猜路径。
