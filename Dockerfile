FROM python:3.10
ENV OR_KEY=""
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "main.py"]