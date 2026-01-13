FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./

RUN npm ci && npm cache clean --force

COPY . .

ENV NODE_ENV=product

RUN npm run build 

FROM node:20-alpine 

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["serve", "-s", "build", "-l", "3000"]
