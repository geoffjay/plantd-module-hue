FROM registry.gitlab.com/plantd/libplantd/module:next
MAINTAINER Geoff Johnson <geoff.jay@gmail.com>

# Create the virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
RUN pip install --upgrade pip
RUN apk update \
    && apk upgrade \
    && apk add \
        cairo-dev \
        gcc \
        gobject-introspection-dev \
        musl-dev \
        pkgconfig

# Add project
RUN mkdir /module
COPY . /module
WORKDIR /module
RUN pip install -r requirements.txt

# Put the overrides file in the venv
RUN cp /usr/local/lib/python3.8/site-packages/gi/overrides/Pd.py \
    /opt/venv/lib/python3.8/site-packages/gi/overrides/

ENV G_MESSAGES_DEBUG=module
ENV PLANTD_MODULE_ARGS=
ENV PLANTD_MODULE_ENDPOINT=tcp://localhost:5555
ENV PLANTD_MODULE_CONFIG_FILE=data/module.json

EXPOSE 5555
# Execute application
CMD python module.py $PLANTD_MODULE_ARGS
