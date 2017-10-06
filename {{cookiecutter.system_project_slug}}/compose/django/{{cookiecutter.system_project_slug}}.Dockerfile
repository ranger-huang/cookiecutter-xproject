FROM ubuntu:16.04
LABEL author.name="Ranger.Huang" \
      author.email="ranger_huang@yeah.net"

COPY ./compose/django/apt-sources.list /etc/apt/sources.list
RUN apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qq -y ntp tzdata && \
    apt-get install -qq -y software-properties-common && \
    {% if cookiecutter.python_version == '3.6' %}
    add-apt-repository ppa:jonathonf/python-3.6 && \
    {% endif %}
    add-apt-repository ppa:saiarcot895/myppa && \
    apt-get -y -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y -qq install apt-fast && \
    DEBIAN_FRONTEND=noninteractive apt-fast install -y -qq build-essential make git \
        libevent-dev \
        {% if cookiecutter.python_version == '3.5' %}
        python3 \
        python3-dev \
        python3-pip \
        {% endif %}

        {% if cookiecutter.python_version == '3.6' %}
        python3.6 \
        python3.6-dev \
        {% endif %}

        libpq-dev \
        mysql-client \
        libmysqlclient-dev \

        zlib1g-dev  \
        libpcre3-dev  \
        libssl-dev  \
        libxml2 \
        libxml2-dev \
        libxslt1.1 \
        libxslt1-dev \
        libgd3 \
        libgd-dev \
        libgeoip-dev \
        libpam0g-dev \
        libgoogle-perftools4 \
        libgoogle-perftools-dev \
        libperl-dev \
        libzbar0 libzbar-dev \

        ##Pillow dependencies
        libtiff5-dev \
        libjpeg8-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libwebp-dev \
        ##django-extensions
        graphviz-dev \

        unzip \
        wget \
        curl \
        unzip \
        vim \
        gunicorn && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN  mkdir -p $HOME/.pip/
COPY ./compose/django/pip.conf $HOME/.pip/pip.conf

{% if cookiecutter.python_version == '3.5' %}
RUN python3.5 -m pip install -U pip gunicorn
{% endif %}

{% if cookiecutter.python_version == '3.6' %}
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6 && \
    python3.6 -m pip install gunicorn
{% endif  %}

ENV LC_ALL=C.UTF-8
ENV TZ=Asia/Shanghai
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/timezone && ntpd

RUN mkdir -p /app
WORKDIR /app
