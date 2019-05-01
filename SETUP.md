# Setup VM

    vagrant up
    vagrant ssh

The rest of the commands are in the vagrant VM.

    sudo apt-get update -y
    sudo apt-get install -y build-essential

## Setup DB Dependencies

    sudo apt-get install postgresql-9.5-postgis-2.2

    # sudo su -
    # wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    # echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >> /etc/apt/sources.list.d/postgresql.list
    # apt-get update -y
    # sudo apt-get install -y \
    #     libpq-dev postgresql-9.3-postgis-2.1 \
    #     postgresql-9.3-postgis-scripts postgresql-contrib-9.3
    # exit

## Setup database

    sudo su - postgres
    psql -c "DROP DATABASE IF EXISTS airbitz_directory;"
    psql -c "DROP DATABASE IF EXISTS template_postgis2;"
    psql -c "DROP ROLE IF EXISTS styx;"

    createdb -E UTF8 template_postgis2.2
    psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis2.2'"
    psql -d template_postgis2.2 -c "CREATE EXTENSION postgis;"
    psql -d template_postgis2.2 -c "GRANT ALL ON geometry_columns TO PUBLIC;"
    psql -d template_postgis2.2 -c "GRANT ALL ON geography_columns TO PUBLIC;"
    psql -d template_postgis2.2 -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

    psql -c "create role styx with login password 'styx'";
    createdb -T template_postgis2.2 airbitz_directory
    psql -d airbitz_directory -c "grant all privileges on database airbitz_directory to styx";
    exit

## Install all needed packages

    curl https://pyenv.run | bash
    echo << EOF >> $HOME/.bashrc 
        export PATH="/home/vagrant/.pyenv/bin:$PATH"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
    EOF

    pyenv install 2.7.8
    pyenv use 2.7.8

    sudo apt-get install -y python-dev python-virtualenv libncurses5-dev  \
        vim git libtiff5-dev libjpeg8-dev zlib1g-dev  \
        libfreetype6-dev libwebp-dev unzip libpq-dev\
        geoip-bin geoip-database 

    sudo apt-get install -y npm redis-server rabbitmq-server
    sudo npm -g install yuglify


## Setup Django

    cd /airbitz
    virtualenv .env
    source .env/bin/activate
    pip install -r /staging/requirements.txt 
