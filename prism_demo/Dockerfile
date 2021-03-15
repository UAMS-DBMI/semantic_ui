FROM node:14 as builder

COPY app/ /app
RUN cd /app && npm install && npm run build

FROM nginx:1.19-alpine
COPY --from=builder /app/build /usr/share/nginx/html
