FROM continuumio/miniconda3:4.10.3

RUN mkdir src

WORKDIR src

COPY environment.yml .
RUN conda env update -f environment.yml -n base

COPY data /data

COPY run.py .

CMD [ "python", "run.py"]

