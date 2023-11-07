FROM docker.io/alpine:3.18 AS development
RUN apk add --no-cache python3 py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango &&\
	python3 -m venv /venv &&\
	/venv/bin/pip install weasyprint flask pyyaml
RUN apk add --no-cache font-inconsolata font-dejavu font-noto font-noto-cjk font-awesome font-noto-extra msttcorefonts-installer
WORKDIR /working
COPY assets /assets
RUN mkdir templates && ln -s /baked-in.html templates/
COPY app.py .
EXPOSE 5000
CMD /venv/bin/flask --debug run -p 5000 --host=0.0.0.0
COPY baked-in.html /
