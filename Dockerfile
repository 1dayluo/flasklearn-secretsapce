FROM python:3.6
WORKDIR ./

COPY requirements.txt ./
RUN pip install --index https://pypi.tuna.tsinghua.edu.cn/simple requests
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["flask","run","--reload"]


