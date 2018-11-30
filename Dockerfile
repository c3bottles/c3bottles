FROM alpine:3.8 as base
RUN apk add -U --no-cache \
    python3 py3-virtualenv cairo


FROM base as builder
WORKDIR /c3bottles
RUN apk add -U --no-cache \
    python3-dev nodejs yarn py3-pip libffi-dev gcc libc-dev zlib-dev postgresql-dev \
    && virtualenv -p python3 /c3bottles/venv
ENV PATH=/c3bottles/venv/bin:$PATH
COPY requirements/production.txt /c3bottles/requirements-production.txt
RUN pip install -r requirements-production.txt --no-cache-dir
COPY package.json yarn.lock /c3bottles/
RUN yarn
COPY . /c3bottles
RUN yarn build ; rm -r /c3bottles/node_modules/


FROM base
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
