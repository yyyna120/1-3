import streamlit as st
import json
import os
from datetime import date

FILE_NAME = "tasks.json"

# 데이터 불러오기
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 데이터 저장
def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# 초기 데이터
tasks = load_tasks()

st.title("📅 일정 관리 앱")

# 일정 추가
st.subheader("일정 추가")

with st.form("task_form"):
    task = st.text_input("일정 내용")
    task_date = st.date_input("날짜", value=date.today())

    submitted = st.form_submit_button("추가")

    if submitted:
        if task.strip() != "":
            tasks.append({
                "task": task,
                "date": str(task_date),
                "done": False
            })

            save_tasks(tasks)
            st.success("일정이 추가되었습니다.")
            st.rerun()
        else:
            st.warning("일정 내용을 입력하세요.")

# 일정 목록
st.subheader("일정 목록")

if len(tasks) == 0:
    st.info("등록된 일정이 없습니다.")

for i, item in enumerate(tasks):

    col1, col2, col3 = st.columns([5, 2, 1])

    with col1:
        checked = st.checkbox(
            f"{item['task']}",
            value=item["done"],
            key=f"check_{i}"
        )

        tasks[i]["done"] = checked

    with col2:
        st.write(item["date"])

    with col3:
        if st.button("삭제", key=f"delete_{i}"):
            tasks.pop(i)
            save_tasks(tasks)
            st.rerun()

# 변경 저장
save_tasks(tasks)
