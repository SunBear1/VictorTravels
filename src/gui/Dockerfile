FROM node:lts-alpine as build-stage

WORKDIR /gui

COPY package*.json ./

COPY tailwind.config.js .

RUN npm install

COPY src src/

COPY public public/

RUN npm run build

FROM nginx:stable-alpine-slim as serve-stage

COPY --from=build-stage /gui/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
