# TEST_READALL.md — 读取能力测试（**4 项，一次测完**）

> ## 这是测试，**不要做学习资料**
>
> 目的：验证你能读到什么、读不到什么。
> **如实汇报，不许编造。** 看不见就说看不见，并贴原始报错。

---

## 准备

```bash
git fetch origin && git merge origin/main
ls -la
ls -la out/
```

---

## 测试 ① 读文字文件（3 个）

随便挑这 3 个读，报告**大小 / 内容量 / 讲了什么**：

```bash
wc -c out/transcript.txt out/slides_unique.txt out/slides_vision.md
head -20 out/transcript.txt
grep -c "^## S" out/slides_vision.md
grep -c "^=== S" out/slides_unique.txt
```

**回答**：
1. `transcript.txt` 多少字节？多少条时间戳？
2. `slides_unique.txt` 多少张幻灯片？
3. `slides_vision.md` 多少张记录？

---

## 测试 ② 读三份旧版 HTML（**先剥离 base64**）

```bash
python3 - <<'EOF'
import re, os
for f in ['心理学12_精讲全解.html', '心理学12_闯关记忆手册.html', '幻灯片总览_高清版.html']:
    p = 'out/' + f
    if not os.path.exists(p):
        print(f, '不存在'); continue
    h = open(p, encoding='utf-8').read()
    before = len(h)
    h2 = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', '[图]', h)
    open('/tmp/' + f + '.txt', 'w', encoding='utf-8').write(h2)
    print(f'{f}: {before//1024} KB → {len(h2)//1024} KB')
EOF

wc -c /tmp/*.txt
head -50 /tmp/心理学12_精讲全解.html.txt
head -50 /tmp/心理学12_闯关记忆手册.html.txt
head -50 /tmp/幻灯片总览_高清版.html.txt
```

**回答**：
1. 三份 HTML 剥离后各多少 KB？
2. **精讲全解**分几幕几节？标题分别是什么？
3. **闯关记忆手册**分几关？有没有擂台、错题本、闪卡？
4. **幻灯片总览**有多少张卡片？每张卡片包含哪些字段？

---

## 测试 ③ 读幻灯片原图（**最关键**）

```bash
mkdir -p /tmp/sl && cd /tmp/sl
unzip -q /path/to/out/frames/slides_102.zip -d slides/
ls slides/*.jpg | wc -l          # 预期 102
```

用 **`functions.shell` 的 `image_path`** 读 `slides/S050.jpg`：

```
functions.shell(command="ls slides/S050.jpg", image_path="/tmp/sl/slides/S050.jpg")
```

> ⚠️ **必须用 `functions.shell` + `image_path`。**
> ❌ 不要用 `functions.display_multimedia`（只返回链接，看不见图）。
> 详见 `HOW_TO_READ_IMAGES.md`。

**回答这三个问题**（**只有真正看见图才能答对**）：

1. 这张图的**标题**是什么？**右上角**有什么？
2. 表格**第 4 行下方**有没有**手写笔迹**？什么**颜色**？写的是什么字？
   （尽量逐字辨认，认不出的写"认不出"）
3. 「xN次」这几个字是什么**颜色**？有没有**下划线**？

> 🚫 **严禁查 `out/slides_unique.txt` 或 `out/slides_vision.md` 来答题。**
> 这三个问题的答案在 OCR 里**一个字都没有**。
> 这一步只测「你的眼睛能不能看见图上的字」。

---

## 测试 ④ 读帧原图

```bash
mkdir -p /tmp/fr && cd /tmp/fr
unzip -q /path/to/out/frames/frames_unique_691.zip -d frames/
ls frames/*.jpg | wc -l          # 预期 691
ls frames/*.jpg | head -3        # 看文件名格式
```

用 `image_path` 读**第 1 张**（按文件名排序的第一张）：

```
functions.shell(command="ls frames/<第一张的文件名>", image_path="/tmp/fr/frames/<第一张的文件名>")
```

**回答**：
1. 这张帧的画面是什么？（是 PPT 还是别的？）
2. 画面上有什么内容？
3. 它和 `slides_102.zip` 里的 `S001.jpg` 是同一张吗？（可以对比一下）

---

## 测试 ⑤ 汇报（**逐项填**）

| # | 测试项 | 结果 |
|---|---|---|
| 1 | 读文字文件 | ✅/❌ |
| 2 | 读三份 HTML（剥离后） | ✅/❌ |
| 3 | **读幻灯片原图（S050 三问）** | ✅/❌ |
| 4 | 读帧原图 | ✅/❌ |
| 5 | 我用了哪个工具看图 | |
| 6 | 有没有遇到报错（贴原文） | |

**最后一句话（必须写）**：

> 我能读到文字文件：能 / 不能。
> 我能读到三份 HTML：能 / 不能。
> 我能读到幻灯片原图：**能 / 不能**（S050 三问答对了 __ / 3 题）。
> 我能读到帧原图：能 / 不能。
> 我一次能看几张图：__ 张。

---

## 提交

```bash
git add -A
git commit -m "test: 读取能力测试（4 项）"
git push -u origin HEAD
```

**只提交测试报告**，不要改其他文件。
报告写成 `out/TEST_READALL_RESULT.md`。
