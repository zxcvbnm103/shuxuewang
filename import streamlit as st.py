import streamlit as st

st.set_page_config(page_title="Markdown笔记", layout="wide")

st.title("Markdown笔记编辑器")

# 读取已保存的 markdown 内容
try:
    with open("my_note.md", "r", encoding="utf-8") as f:
        default_md = f.read()
except FileNotFoundError:
    default_md = ""

md_content = st.text_area("编辑你的 Markdown 内容：", value=default_md, height=300)

if st.button("保存笔记"):
    with open("my_note.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    st.success("笔记已保存！")

st.subheader("Markdown预览：")
st.markdown(md_content)