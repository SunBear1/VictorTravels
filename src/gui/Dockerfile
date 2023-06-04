FROM node:lts-alpine3.18 as build-stage

WORKDIR /gui

COPY package*.json ./

COPY tailwind.config.js .

RUN npm install

COPY src src/

COPY public public/

RUN npm run build

FROM nginx:stable-alpine-slim as serve-stage

COPY --from=build-stage /gui/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
