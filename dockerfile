FROM node:alpine
RUN apk update && apk install -y python3 python3-pip
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN pip install BeautifulSoup4 requests
COPY . .
RUN chmod +x boot.sh
EXPOSE ${PORT}
CMD ["./boot.sh"]
