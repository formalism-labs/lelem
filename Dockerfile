
FROM ubuntu:noble

SHELL ["/bin/bash", "-l", "-c"]

WORKDIR /build

COPY --from=classico . /build/classico
COPY requirements.txt .

RUN ./classico/bin/getget
RUN VERSION=3.13 ./classico/bin/getpy
RUN ./classico/bin/getgcc
RUN ./classico/bin/getpudb
RUN apt-get install -y mc vim htop

RUN uv pip install -r requirements.txt

CMD ["/bin/bash", "-l"]
