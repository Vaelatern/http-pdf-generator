FROM docker.io/alpine:3.18 AS development
RUN apk add --no-cache python3 py3-pip libreoffice openjdk11 &&\
	python3 -m venv /venv &&\
	/venv/bin/pip install flask pyyaml docx2pdf docxtpl
RUN apk add --no-cache font-inconsolata font-dejavu font-noto font-noto-cjk font-awesome font-noto-extra msttcorefonts-installer && update-ms-fonts && fc-cache -f
WORKDIR /working
COPY app.py .
EXPOSE 5000
CMD /venv/bin/flask --debug run -p 5000 --host=0.0.0.0
COPY baked-in.docx .
