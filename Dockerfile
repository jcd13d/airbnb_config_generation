FROM python:3

ADD generate_id_scraper_configs.py /
ADD price_functions /price_functions
ADD occupancy_functions /occupancy_functions
ADD id_functions /id_functions
ADD requirements.txt /

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

#CMD ["curl", "169.254.170.2\$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"]
CMD ["python", "generate_id_scraper_configs.py"]

# docker buildx build --platform=linux/amd64 -t config_creator .
