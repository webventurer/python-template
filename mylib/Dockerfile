FROM python:3.13.2

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHON_BUFFERED=true \
    PYTHONPATH=/mylib:/mylib/app:/mylib/thirdparty

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y build-essential nmap vim curl nginx sudo iputils-ping && \
    apt-get autoremove -y && \
    apt-get autoclean -y

WORKDIR /mylib

ARG user_id=1001
ARG group_id=1001
RUN groupadd -g $group_id app && \
    useradd --system -u $user_id -g app --home-dir /app app

RUN echo "app ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY requirements.txt .
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt

COPY Makefile .
COPY thirdparty ./thirdparty
RUN make install-local

RUN curl -sfS https://dotenvx.sh/install.sh | sh

COPY . /mylib

RUN chown -R app:app /mylib
RUN chmod +x app/api/docker-entrypoint.sh

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/lib/nginx && \
    mkdir -p /var/lib/nginx/body && \
    mkdir -p /var/log/nginx && \
    mkdir -p /run && \
    chown -R app:app /var/lib/nginx && \
    chown -R app:app /var/log/nginx && \
    chown -R app:app /run

USER app

EXPOSE 80

ENTRYPOINT ["dotenvx", "run", "--env-file", ".env.vault", "--", "app/api/docker-entrypoint.sh"]

# CMD ["tail", "-f", "/dev/null"]
