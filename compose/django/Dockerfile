FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN apt-get update && apt-get install -qqy apt-utils && apt-get install -qqy libxml2-utils

RUN pip install -r /requirements/production.txt \
    && groupadd -r django \
    && useradd -r -g django django

RUN mkdir -p /etc/xml \
    && bash -c "$(curl -fsSL https://raw.githubusercontent.com/scieloorg/packtools/master/scripts/install_xml_catalog.sh)"

COPY . /app
RUN mkdir /app/media /app/static
RUN chown -R django /app

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

VOLUME /app/media
VOLUME /app/static
WORKDIR /app

USER django

ENTRYPOINT ["/entrypoint.sh"]
