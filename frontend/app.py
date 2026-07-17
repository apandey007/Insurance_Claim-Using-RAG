import streamlit as st
import requests

st.write("Hello Suditi")

st.set_page_config(page_title="PDF Chat App")

st.title("📄 Chat with PDF")

# Chat message
message = st.text_input("Enter your question")

# PDF uploader
uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Send"):

    if not message:
        st.warning("Please enter a message")
    else:

        files = []

        # Convert uploaded PDFs for requests
        if uploaded_files:
            for file in uploaded_files:
                files.append(
                    (
                        "files",
                        (
                            file.name,
                            file.getvalue(),
                            "application/pdf"
                        )
                    )
                )

        # Form data
        data = {
            "message": message
        }

        try:
            response = requests.post(
                "http://localhost:8000/api/chat",
                data=data,
                files=files
            )

            result = response.json()

            st.success("Response received")

            st.write("### Backend Response")
            st.json(result)

        except Exception as e:
            st.error(str(e))