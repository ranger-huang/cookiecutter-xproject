FROM {{cookiecutter.system_project_slug}}:latest
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
RUN mkdir -p /appsrc
RUN mkdir -p $HOME/.ssh
COPY ./compose/django/ssh.d /root/.ssh
RUN sed -i 's/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g' /etc/ssh/ssh_config | true
RUN chmod 0600 /root/.ssh/id_rsa | true

COPY ./requirements /requirements
RUN pip3 install --src /appsrc -r /requirements/local.txt

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start-dev.sh /start-dev.sh
RUN sed -i 's/\r//' /start-dev.sh
RUN chmod +x /start-dev.sh

WORKDIR /app

#RUN git clone https://github.com/wxpay/WXPay-SDK-Python.git && \
#     cd WXPay-SDK-Python && echo "" > README.rst && python3 setup.py install && \
#     cd - && rm -rf WXPay-SDK-Python

RUN chmod 0600 /root/.ssh/id_rsa
RUN pip3 install --upgrade --src /appsrc -r /requirements/xingzhe.txt

ENTRYPOINT ["/entrypoint.sh"]
