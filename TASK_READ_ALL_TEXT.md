# TASK_READ_ALL_TEXT.md — 阶段 0：把全部文字素材读一遍

> ## 这是「开工前的清点」，**必须先做**
>
> 目标：**把仓库里所有文字类文件全部读一遍，并汇报每份讲了什么、有多少内容。**
>
> **不做手册、不改文件。** 只读 + 汇报。
> **不许编造** —— 没读到的就说没读到。

---

## 一、准备

```bash
# 同步（必须！工作区不会自动拉新文件）
git fetch origin && git merge origin/main

# 看根目录
ls -la
ls -la out/
ls -la scripts/
```

---

## 二、逐份读取并汇报

### 2.1 核心素材（`out/` 目录）

对下面每一份，**读完后汇报：文件大小 / 内容量 / 讲了什么 / 结构长什么样**。

| # | 文件 | 怎么读 | 汇报什么 |
|---|---|---|---|
| 1 | `out/transcript.txt` | 直接读 | 多少字？多少条时间戳？覆盖多长时间？开头和结尾各讲什么？ |
| 2 | `out/slides_unique.txt` | 直接读 | 多少个 `S###` 小节？每节结构？内容质量如何？ |
| 3 | `out/ocr_all.jsonl` | 逐行 JSON 解析 | 多少条记录？每条的字段有哪些？ |
| 4 | `out/slides_index.md` | 直接读 | 多少行？表格有哪些列？ |
| 5 | `out/slides_index.json` | JSON 解析 | 数组多长？第一条长什么样？ |
| 6 | `out/slides/manifest.md` | 直接读 | 多少条？列了哪些字段？ |
| 7 | `out/uniq_meta.json` | JSON 解析 | 结构是什么？有多少条？ |
| 8 | `out/asr_raw.jsonl` | 逐行 JSON 解析 | 多少条？字段有哪些？ |

**现成命令**：

```bash
echo "=== transcript.txt ==="
wc -c -l out/transcript.txt
head -5 out/transcript.txt
tail -3 out/transcript.txt

echo "=== slides_unique.txt ==="
wc -c out/slides_unique.txt
grep -c "^=== S" out/slides_unique.txt

echo "=== ocr_all.jsonl ==="
wc -l out/ocr_all.jsonl
python3 -c "
import json
rows=[json.loads(l) for l in open('out/ocr_all.jsonl',encoding='utf-8') if l.strip()]
print('记录数:', len(rows))
print('字段:', list(rows[0].keys()))
print('第一条:', json.dumps(rows[0], ensure_ascii=False)[:200])
"

echo "=== slides_index.md / .json ==="
wc -l out/slides_index.md
python3 -c "
import json
d=json.load(open('out/slides_index.json',encoding='utf-8'))
print('长度:', len(d)); print('第一条:', json.dumps(d[0], ensure_ascii=False)[:200])
"

echo "=== manifest / uniq_meta / asr_raw ==="
wc -l out/slides/manifest.md
python3 -c "
import json
d=json.load(open('out/uniq_meta.json',encoding='utf-8'))
print('uniq_meta 类型:', type(d).__name__, '长度:', len(d))
"
wc -l out/asr_raw.jsonl
```

### 2.2 幻灯片总览 HTML（**注意：要先剥离 base64**）

`out/幻灯片总览_高清版.html` 有 6 MB，**里面大部分是 base64 图片**，
直接读会浪费巨量 token。**先剥离**：

```bash
python3 -c "
import re
h=open('out/幻灯片总览_高清版.html',encoding='utf-8').read()
print('原始大小:', len(h))
h2=re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+','[图]',h)
open('/tmp/overview.txt','w',encoding='utf-8').write(h2)
print('剥离后:', len(h2))
print('卡片数:', h2.count(chr(60)+'figure class=' + chr(39) + 'card' + chr(39)))
"
wc -c /tmp/overview.txt
head -60 /tmp/overview.txt
```

**汇报**：多少张卡片？每张卡片有哪些信息（图 / 时间 / OCR / 讲解）？

### 2.3 文档（根目录）

| 文件 | 汇报什么 |
|---|---|
| `QUICKSTART.md` | 开工指引，讲了什么流程 |
| `REQUIREMENTS.md` | 考生要求 + 验收标准，**逐条列出六条标准** |
| `TASK.md` | 素材清单与读取方法 |
| `TASK_READ_FRAMES.md` | 691 帧读取作业书 |
| `TASK_READ_BATCH.md` | 102 张读取作业书（备选） |
| `HOW_TO_READ_IMAGES.md` | 读图方法，**关键是什么** |
| `CLAUDE.md` | 沙箱操作，**第 0 节讲了哪三件事** |
| `BRIEF.md` | 制作规格参考 |
| `PROBE.md` / `PROBE2.md` | 环境探针记录 |
| `README.md` | 项目说明 |

```bash
for f in QUICKSTART.md REQUIREMENTS.md TASK.md TASK_READ_FRAMES.md \
         TASK_READ_BATCH.md HOW_TO_READ_IMAGES.md CLAUDE.md BRIEF.md \
         PROBE.md PROBE2.md README.md; do
  echo "===== $f ($(wc -c < "$f") 字节) ====="
  head -25 "$f"
  echo
done
```

### 2.4 工具链（`scripts/` 目录，14 个文件）

```bash
ls -la scripts/
head -60 scripts/SKILL.md          # 完整流水线说明
head -20 scripts/run_pipeline.py   # 主流水线
```

**汇报**：每个脚本是干什么的？一句话概括。

---

## 三、汇报格式（**逐项填**）

### 3.1 核心素材

| # | 文件 | 大小 | 内容量 | 讲了什么 | 读到没 |
|---|---|---|---|---|---|
| 1 | `out/transcript.txt` | | ___ 字 / ___ 条 | | ✅/❌ |
| 2 | `out/slides_unique.txt` | | ___ 张幻灯片 | | ✅/❌ |
| 3 | `out/ocr_all.jsonl` | | ___ 条 | | ✅/❌ |
| 4 | `out/slides_index.md` | | ___ 行 | | ✅/❌ |
| 5 | `out/slides_index.json` | | ___ 条 | | ✅/❌ |
| 6 | `out/slides/manifest.md` | | ___ 条 | | ✅/❌ |
| 7 | `out/uniq_meta.json` | | ___ 条 | | ✅/❌ |
| 8 | `out/asr_raw.jsonl` | | ___ 条 | | ✅/❌ |
| 9 | `out/幻灯片总览_高清版.html` | 6 MB | ___ 张卡片 | | ✅/❌ |

### 3.2 文档

| 文件 | 一句话概括 | 读到没 |
|---|---|---|
| QUICKSTART.md | | ✅/❌ |
| REQUIREMENTS.md | | ✅/❌ |
| TASK.md | | ✅/❌ |
| TASK_READ_FRAMES.md | | ✅/❌ |
| TASK_READ_BATCH.md | | ✅/❌ |
| HOW_TO_READ_IMAGES.md | | ✅/❌ |
| CLAUDE.md | | ✅/❌ |
| BRIEF.md | | ✅/❌ |
| PROBE.md / PROBE2.md | | ✅/❌ |
| README.md | | ✅/❌ |

### 3.3 工具链

| 脚本 | 作用 | 读到没 |
|---|---|---|
| scripts/SKILL.md | | ✅/❌ |
| （其余 13 个） | | ✅/❌ |

---

## 四、最后一句话（必须写）

> 我读完了 __ / __ 份文字素材和文档。
> 没读到的有：____（没有就写"无"）。
> 我理解的这一讲范围是：____。

---

## 五、提交

把汇报写成 `out/STAGE0_INVENTORY.md`，然后：

```bash
git add out/STAGE0_INVENTORY.md
git commit -m "docs: 阶段 0 —— 全部文字素材清点"
git push -u origin HEAD
```

**只新增这一个文件**，不要改其他任何文件。
