import streamlit as st
import subprocess
from week_4.codeConvertor import CodeConvertor


def week_task():
    st.title("Python → C++ Converter")
    if "converted_cpp" not in st.session_state:
        st.session_state.converted_cpp = ""
    convertor = CodeConvertor("LLAMA")
    pi = """
import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result

start_time = time.time()
result = calculate(200_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time: {(end_time - start_time):.6f} seconds")
        """
    cols1, cols2 = st.columns(2)
    with cols1:
        cols1.header("Python Code")
        py_input = st.text_area(
            "Enter your Python code here:",
            value=pi,
            height="content"
        )
        if st.button("▶️ Execute Python"):
            with open("week_4/temp.py", "w") as f:
                f.write(pi)
            run_result = subprocess.run(
                ["python3", "week_4/temp.py"],
                capture_output=True,
                text=True,
            )
            if run_result.returncode == 0:
                st.success("✅ Python executed successfully!")
                st.code(run_result.stdout)
            else:
                st.error(f"❌ Python error:\n{run_result.stderr}")


    if st.button("Convert to C++"):
        st.session_state.converted_cpp = convertor.convert(py_input)

    with cols2:
        st.header("C++")
        if st.session_state.converted_cpp:
            st.code(st.session_state.converted_cpp)
        if st.button("Execute"):
            compile_result = subprocess.run(['g++', 'week_4/main.cpp', '-o', 'week_4/main'], capture_output=True, text=True)
            if compile_result.returncode != 0:
                st.error(f"Compilation failed: \n {compile_result.stderr}")
            else:
                run_result = subprocess.run(['week_4/main'], capture_output=True, text=True)
                st.code(f"Program output: \n {run_result.stdout}")