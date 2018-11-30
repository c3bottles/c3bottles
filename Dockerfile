FROM alpine:latest as builder
WORKDIR /c3bottles
RUN apk add -U --no-cache \
    python3-dev nodejs yarn py3-pip py3-virtualenv libffi-dev gcc libc-dev zlib-dev jpeg-dev cairo postgresql-dev \
    && virtualenv -p python3 /c3bottles/venv
ENV PATH=/c3bottles/venv/bin:$PATH
COPY requirements.txt /c3bottles
RUN pip3 install -r requirements.txt --no-cache-dir
COPY package.json yarn.lock /c3bottles/
RUN yarn
COPY . /c3bottles
RUN yarn build


FROM python:3.6-alpine
RUN apk add -U --no-cache \
    py3-virtualenv cairo
COPY --from=builder /usr/lib/libpq.so.5 /usr/lib/libpq.so.5
COPY --from=builder /usr/lib/libldap_r-2.4.so.2 /usr/lib/libldap_r-2.4.so.2
COPY --from=builder /usr/lib/liblber-2.4.so.2 /usr/lib/liblber-2.4.so.2
COPY --from=builder /usr/lib/libsasl2.so.3 /usr/lib/libsasl2.so.3
COPY --from=builder /c3bottles /c3bottles
WORKDIR /c3bottles
ENV PATH=/c3bottles/venv/bin:$PATH
EXPOSE 5000
EXPOSE 9567
CMD gunicorn -b 0.0.0.0:5000 wsgi
