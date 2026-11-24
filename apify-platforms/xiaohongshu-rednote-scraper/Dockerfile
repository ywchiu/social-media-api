FROM apify/actor-python:3.12
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
ENV LARGITDATA_PLATFORM=xiaohongshu
CMD ["python3", "-m", "src"]
