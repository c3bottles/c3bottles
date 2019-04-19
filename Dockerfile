FROM alpine:3.8 as base
RUN apk add -U --no-cache \
    python3 py3-virtualenv cairo libpq


FROM base as builder
WORKDIR /c3bottles
RUN apk add -U --no-cache \
    python3-dev nodejs yarn py3-pip libffi-dev gcc libc-dev zlib-dev postgresql-dev \
    && virtualenv -p python3 /c3bottles/venv
ENV PATH=/c3bottles/venv/bin:$PATH
COPY requirements/docker.txt requirements/production.txt /c3bottles/requirements/
RUN pip install -r requirements/docker.txt --no-cache-dir
COPY package.json yarn.lock /c3bottles/
RUN yarn
COPY . /c3bottles
RUN yarn build ; rm -r /c3bottles/node_modules/


FROM base
RUN apk add --no-cache fontconfig wget \
    && mkdir -p /usr/share/fonts \
    && wget https://github.com/google/fonts/raw/master/ofl/montserrat/Montserrat-Black.ttf -O /usr/share/fonts/Montserrat-Black.ttf \
    && wget https://github.com/google/fonts/raw/master/ofl/montserrat/Montserrat-Light.ttf -O /usr/share/fonts/Montserrat-Light.ttf \
    && apk del wget
RUN apk --no-cache add msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f
COPY --from=builder /c3bottles /c3bottles
WORKDIR /c3bottles
ENV PATH=/c3bottles/venv/bin:$PATH
EXPOSE 5000
EXPOSE 9567
CMD gunicorn -b 0.0.0.0:5000 wsgi
