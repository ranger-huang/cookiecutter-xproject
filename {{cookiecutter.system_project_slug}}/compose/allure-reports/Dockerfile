FROM openjdk:8
LABEL author.name="Ranger.Huang" \
      author.email="ranger_huang@yeah.net"


RUN apt-get -qq update && \
    apt-get -qq install unzip wget && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ENV ALLURE_VERSION=2.3.3
RUN wget https://dl.bintray.com/qameta/generic/io/qameta/allure/allure/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip
RUN unzip allure-${ALLURE_VERSION}.zip -d /usr/local/
RUN ln -s /usr/local/allure-${ALLURE_VERSION} /usr/local/allure
ENV PATH /usr/local/allure/bin:$PATH
RUN rm -rf allure-${ALLURE_VERSION}.zip

RUN mkdir -p /reports
WORKDIR /reports

VOLUME /reports
EXPOSE 5200
ENTRYPOINT allure serve -p 5200 /reports
