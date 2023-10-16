FROM node:20-slim AS builder

WORKDIR /frontend

COPY package*.json /frontend
RUN npm clean-install

COPY . /frontend
RUN npm run build --if-present

WORKDIR /

FROM nginx:1.25 AS runner
COPY --from=builder frontend/build/ /usr/share/nginx/html
