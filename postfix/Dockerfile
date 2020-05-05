FROM alpine:latest
# python3 shared with most images
RUN apk add --no-cache \
    python3 py3-pip git bash \
  && pip3 install --upgrade pip

# Image specific layers under this line
RUN apk add --no-cache postfix postfix-pcre cyrus-sasl-plain

COPY postfix/conf /etc/postfix

COPY postfix/start.py /


#EXPOSE 25/tcp 10025/tcp
EXPOSE 25/tcp
VOLUME ["/queue"]


ENTRYPOINT ["/usr/bin/python3", "/start.py"]
#CMD /start.py

#HEALTHCHECK --start-period=350s CMD echo QUIT|nc localhost 25|grep "220 .* ESMTP Postfix"
