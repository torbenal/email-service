FROM node:latest AS build

WORKDIR /app
ADD . /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn install

RUN yarn build

FROM nginx:1.17-alpine

COPY --from=build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]