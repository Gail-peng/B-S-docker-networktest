# 第一阶段：构建前端
FROM node as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build  # 构建Vue应用

# 第二阶段：配置Nginx
FROM nginx
COPY --from=build /app/dist /usr/share/nginx/html  
COPY ./nginx/default.conf /etc/nginx/conf.d/       
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]