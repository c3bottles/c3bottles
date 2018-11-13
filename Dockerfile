FROM alpine:latest
COPY . /c3bottles
WORKDIR /c3bottles
RUN apk add -U --no-cache python3-dev nodejs yarn py3-pip libffi-dev gcc libc-dev zlib-dev jpeg-dev cairo postgresql-dev  
RUN rm -rf /tmp/*
RUN pip3 install -r requirements.txt --no-cache-dir 
RUN yarn install
RUN yarn run build
EXPOSE 5000
CMD gunicorn -b 0.0.0.0:5000 wsgi