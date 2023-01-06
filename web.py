import streamlit as st
import functions
import pandas

todos = functions.get_todos()

st.set_page_config(
    page_title="ToDo App",
    page_icon="random",
    initial_sidebar_state="expanded",
)


# convert CSV into a DF to be able to generate CSV file for download
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


# Part of the generate CSV file for download function
df = pandas.read_csv("todos.txt")
csv = convert_df(df)


def add_todo():
    todo = st.session_state["new_todo"]
    todo = todo.title() + '\n'
    todos.append(todo)
    functions.write_todos(todos)


st.title("My ToDo App")

st.subheader("This is my To Do Web App.")
st.write("This app is to increase your productivity.")

for index, todo in enumerate(todos):
    checkbox = st.checkbox(todo, key=todo)
    if checkbox:
        todos.pop(index).strip('\n')
        functions.write_todos(todos)
        del st.session_state[todo]
        st.experimental_rerun()

st.text_input(label="", placeholder="Add New ToDo...", on_change=add_todo,
              key='new_todo')

# V1 works but it not optimal - potential improvement change todos into csv file for smoother process.
csv_download = st.download_button(label="Download ToDos", data=csv, file_name="ToDos.xlsx",
                                  mime="application/vnd.ms-excel")