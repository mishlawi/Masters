FROM ubuntu
RUN apt update
RUN apt install -y software-properties-common
RUN apt install -y nodejs
RUN apt install -y npm
RUN apt install -y git
RUN npm i -g yarn
RUN git clone https://github.com/Requarks/wiki
WORKDIR "/wiki"
RUN yarn
RUN mv config.sample.yml config.yml
COPY ./edit_configs.sh/ /wiki/
RUN chmod +x edit_configs.sh 
EXPOSE 3000
CMD yarn dev
