FROM {{cookiecutter.system_project_slug}}:latest
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
RUN mkdir -p /appsrc
RUN mkdir -p $HOME/.ssh
COPY ./compose/django/ssh.d /root/.ssh
RUN sed -i 's/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g' /etc/ssh/ssh_config | true
RUN chmod 0600 /root/.ssh/id_rsa | true

COPY ./requirements /requirements
RUN pip3 install --src /appsrc -r /requirements/test.txt

COPY ./compose/django/entrypoint-test.sh /entrypoint-test.sh
RUN sed -i 's/\r//' /entrypoint-test.sh
RUN chmod +x /entrypoint-test.sh

COPY ./compose/django/start-test.sh /start-test.sh
RUN sed -i 's/\r//' /start-test.sh
RUN chmod +x /start-test.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint-test.sh", "/start-test.sh"]
