FROM {{cookiecutter.system_project_slug}}:latest
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
RUN mkdir -p /appsrc
RUN mkdir -p $HOME/.ssh
COPY ./compose/django/ssh.d /root/.ssh
RUN sed -i 's/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g' /etc/ssh/ssh_config | true
RUN chmod 0600 /root/.ssh/id_rsa | true

COPY ./requirements /requirements
RUN pip3 install -r /requirements/production.txt \
    && groupadd -r django \
    && useradd -r -g django django

COPY . /app
RUN chown -R django /app

COPY ./compose/django/gunicorn_conf.py /gunicorn_conf.py
COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

RUN pip3 install --upgrade --src /appsrc -r /requirements/xingzhe.txt

ENTRYPOINT ["/entrypoint.sh"]
