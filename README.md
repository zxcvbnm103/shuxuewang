# Markdown笔记编辑器

这是一个基于 Streamlit 的简单 Markdown 笔记编辑器，可以在网页上编辑和实时预览 Markdown 内容。

## 功能
- 编辑 Markdown 内容
- 实时预览 Markdown 效果
- 保存笔记到本地 `my_note.md` 文件
- 重新打开自动加载已保存内容

## 使用方法
1. 安装依赖：
   ```bash
   pip install streamlit
   ```
2. 运行应用：
   ```bash
   streamlit run import streamlit as st.py
   ```
3. 在浏览器中访问显示的地址，即可使用笔记编辑器。

## 文件说明
- `import streamlit as st.py`：主程序文件，包含全部功能代码
- `my_note.md`：保存的 Markdown 笔记内容

## 注意事项
- 请确保 Python 环境已安装 Streamlit
- 文件名可根据实际情况修改

---
如需更多功能或界面美化，可进一步扩展代码。
