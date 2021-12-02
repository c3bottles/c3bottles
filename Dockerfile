FROM alpine:3.15 as base
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DISABLE_PIP_VERSION_CHECK=true
RUN apk add -U --no-cache \
    python3 \
    cairo \
    libpq \
    libstdc++ \
    && adduser --disabled-password c3bottles


FROM base as builder
WORKDIR /c3bottles
RUN apk add -U --no-cache \
    python3-dev \
    py3-virtualenv \
    nodejs \
    yarn \
    py3-pip \
    libffi-dev \
    gcc \
    g++ \
    libc-dev \
    zlib-dev \
    postgresql-dev \
    && chown c3bottles:c3bottles /c3bottles
COPY --chown=c3bottles:c3bottles requirements/docker.txt requirements/production.txt /c3bottles/requirements/
USER c3bottles
RUN virtualenv -p python3 /c3bottles/venv
ENV PATH=/c3bottles/venv/bin:$PATH
RUN pip install -r requirements/docker.txt
COPY --chown=c3bottles:c3bottles package.json yarn.lock /c3bottles/
RUN yarn
COPY --chown=c3bottles:c3bottles . /c3bottles
RUN yarn build && rm -r /c3bottles/node_modules/


FROM base as fontloader
RUN apk add --no-cache wget zip \
    && apk add --no-cache --virtual .msttcorefonts msttcorefonts-installer \
    && update-ms-fonts \
    && apk del --no-cache .msttcorefonts \
    && mkdir -p /usr/share/fonts \
    && wget https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Black.ttf -O /usr/share/fonts/Montserrat-Black.ttf \
    && wget https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Light.ttf -O /usr/share/fonts/Montserrat-Light.ttf \
    && wget https://events.ccc.de/congress/2019/wiki/images/6/61/Blackout_Midnight_Umlauts.ttf.zip -O /usr/share/fonts/Blackout_Midnight_Umlauts.ttf.zip \
    && cd /usr/share/fonts && unzip Blackout_Midnight_Umlauts.ttf.zip && rm -rf Blackout_Midnight_Umlauts.ttf.zip


FROM base AS testrunner
COPY --from=builder /c3bottles /c3bottles
WORKDIR /c3bottles
ENV PATH=/c3bottles/venv/bin:$PATH
RUN pip install pytest flask-webtest
USER c3bottles


FROM base
COPY --from=fontloader /usr/share/fonts/ /usr/share/fonts/
COPY --from=builder /c3bottles /c3bottles
RUN fc-cache -f
USER c3bottles
WORKDIR /c3bottles
VOLUME /c3bottles/static
ENV PATH=/c3bottles/venv/bin:$PATH
EXPOSE 5000
EXPOSE 9567
CMD gunicorn -b 0.0.0.0:5000 wsgi
