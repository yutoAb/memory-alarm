# frontend/Dockerfile
FROM node:22-alpine

# 作業ディレクトリ
WORKDIR /app

# 依存インストール（キャッシュ最適化）
COPY package.json package-lock.json* ./
RUN npm ci

# ソース投入
COPY . .

# Vite dev server
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
