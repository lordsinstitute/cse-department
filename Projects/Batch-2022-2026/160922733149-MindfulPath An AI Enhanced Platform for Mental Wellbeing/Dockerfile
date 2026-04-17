FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 5006

ENV NODE_ENV=production
ENV PORT=5006
ENV JWT_SECRET=mindfulpath_docker_secret_key
ENV JWT_EXPIRES_IN=30d

CMD ["node", "server.js"]
