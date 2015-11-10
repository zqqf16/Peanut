 一个静态博客生成工具，由[zqqf16.github.com](https://github.com/zqqf16/zqqf16.github.com)演变而来，目前正在开发中~

### 安装

``` bash
git clone https://github.com/zqqf16/Peanut.git
cd peanut
sudo python setup.py install
```

### 使用

#### 初始化

``` bash
cd blog
peanut init
```

#### 写文章

``` markdown
---
title: Hello world
tag: test
date: 2015-11-11
---

Hello World!
```

保存到 “drafts/hello_world.md”

#### 生成 HTML

``` bash
peanut                   
👉  Loading configurations...
👉  Verifing configurations...
👉  Generating...
👉  Loading drafts...
🍻  1 posts total
👉  Rendering files...
```

#### 预览

``` bash
python -m SimpleHTTPServer
```

或:

``` bash
python3 -m http.server
```

### 依赖

- Jinja2
- Markdown
- Pygments
- PyYAML
- six
- docopt

### License

The MIT License (MIT)

Copyright (c) 2015 zqqf16

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

