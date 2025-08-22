# base image
FROM Python:3.10.8
# working directory
WORKDIR /pdf_chatbot
# copy
COPY . /pdf_chatbot/
# run
RUN pip install -r requirements.txt
# port
EXPOSE 8501


# commmand
CMD ["python", "streamlit.py"]
