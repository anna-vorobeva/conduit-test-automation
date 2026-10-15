# Conduit frontend: official Angular implementation pinned to a known-good commit,
# built with bun and served by nginx (which also proxies /api to the backend).

FROM oven/bun:1 AS build

ARG FRONTEND_REPO=https://github.com/realworld-apps/angular-realworld-example-app.git
ARG FRONTEND_REF=dd99ed2cf39c805d719f943c5d7061a5683d98a8

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# The build needs the "realworld" submodule (shared theme and images)
RUN git init -q . \
    && git fetch -q --depth 1 "$FRONTEND_REPO" "$FRONTEND_REF" \
    && git checkout -q FETCH_HEAD \
    && git submodule update --init --depth 1 --quiet

# --ignore-scripts skips husky, which expects a real git checkout
RUN bun install --frozen-lockfile --ignore-scripts

# Upstream hardcodes the public demo API; make requests same-origin so nginx can proxy them
RUN sed -i 's#https://api.realworld.show/api#/api#' src/app/core/interceptors/api.interceptor.ts \
    && grep -q "'/api\${req.url}'" src/app/core/interceptors/api.interceptor.ts || grep -q '`/api' src/app/core/interceptors/api.interceptor.ts

RUN bun run build


FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/dist/angular-conduit/browser /usr/share/nginx/html

EXPOSE 80
