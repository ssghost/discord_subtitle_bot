FROM gorialis/discord.py:latest

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "subtitlebot.py"]