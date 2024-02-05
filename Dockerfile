# 使用官方的 Node.js 作为基础镜像
FROM node:lts as build-stage

# 设置工作目录
WORKDIR /app/frontend

# 复制`package.json`和`package-lock.json` (如果可用)
COPY ./package*.json .

# 安装项目依赖
RUN npm install

# 复制项目文件和文件夹到工作目录
COPY . .

# 构建应用为生产版本
RUN npm run build

# 暴露端口（如果应用程序在容器内部监听特定端口）
EXPOSE 8080

# 启动应用程序
CMD ["npm", "run", "serve"]