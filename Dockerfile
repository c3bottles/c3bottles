FROM alpine:3.10 as base
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


FROM base as fontloader
RUN apk add --no-cache wget \
    && mkdir -p /usr/share/fonts \
    && wget https://github.com/google/fonts/raw/master/ofl/montserrat/Montserrat-Black.ttf -O /usr/share/fonts/Montserrat-Black.ttf \
    && wget https://github.com/google/fonts/raw/master/ofl/montserrat/Montserrat-Light.ttf -O /usr/share/fonts/Montserrat-Light.ttf 


FROM base
COPY --from=fontloader /usr/share/fonts/Montserrat-Light.ttf /usr/share/fonts/Montserrat-Light.ttf
COPY --from=fontloader /usr/share/fonts/Montserrat-Black.ttf /usr/share/fonts/Montserrat-Black.ttf
RUN apk --no-cache add msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f
RUN find / -name .exe -exec rm -rf {} \;
RUN addgroup -S c3bottles && adduser -S -G c3bottles c3bottles 
COPY --from=builder --chown=c3bottles:c3bottles /c3bottles /c3bottles
USER c3bottles
WORKDIR /c3bottles
VOLUME /c3bottles/static
ENV PATH=/c3bottles/venv/bin:$PATH
EXPOSE 5000
EXPOSE 9567
CMD gunicorn -b 0.0.0.0:5000 wsgi
