FROM node:20-alpine

WORKDIR /app

COPY apps/admin/package*.json ./apps/admin/
RUN cd apps/admin && npm install

COPY . .

WORKDIR /app/apps/admin

EXPOSE 3000

CMD ["npm", "run", "dev"]
