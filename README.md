# 此项目是用于记录前后段通过docker部署后，前端服务和后端服务之间的网络问题

因为在之前的使用经验中，几乎不配置nginx相关的配置，前端直接使用后端的主机IP外加外部端口进行联通，这样的方式不适合生产环境。因此，特使用次项目记录自己的学习过程。

## 1.通过docker部署，将两个服务联通到一个网络中，并且使用服务名和内部container的端口号进行配置，发现使用浏览器访问前端后，触发相应的接口并不会将请求转发到后端。

那么这是因为什么呢？原因可能有两种：

跨域（CORS）限制
浏览器有严格的同源策略（Same-Origin Policy），当前端页面的域名 / 端口与后端 API 的域名 / 端口不一致时，浏览器会阻止跨域请求，即使前端容器内部能通过服务名访问后端（容器间网络互通），浏览器也会报错。
例如：前端在浏览器中访问的地址是 http://localhost:8080，而后端 API 请求的是 http://backend:5000（服务名），两者域名 / 端口不同，触发跨域限制。

前端请求路径错误
若前端请求时直接使用后端服务名（如 http://backend:5000/hello），浏览器会将 backend 解析为无效域名（浏览器无法识别 Docker 内部服务名），导致请求失败。
容器内部能通过 curl backend:5000 访问，是因为 Docker 的 DNS 服务在容器网络内生效，但浏览器运行在宿主机，无法解析 Docker 内部服务名。

## 解决方法

1.后端配置跨域

2.在 Docker 中添加 Nginx 服务，作为前端和后端的中间层，统一请求域名 / 端口，避免跨域。

## 关于Nginx的配置

在 Nginx 配置中，路径匹配规则（如/back和/back/）和代理目标地址（如http://backend:5000和http://backend:5000/）的末尾斜杠（/）会影响请求路径的处理方式。以下是详细区别和示例：

一、location /back vs location /back/

1. location /back（不带末尾斜杠）
   
匹配规则：
匹配所有以 /back 开头的路径，无论其后是否有斜杠。
示例匹配：

```
/back
/back/
/back/api
/back/test/123
```

2. location /back/（带末尾斜杠）
   
匹配规则：
严格匹配以 /back/ 开头的路径，必须包含斜杠。
示例匹配：

```
/back/
/back/api
/back/test/123
不匹配：
/back（缺少末尾斜杠）
```

proxy_pass http://backend:5000 vs proxy_pass http://backend:5000/

1. proxy_pass http://backend:5000（不带末尾斜杠）

路径处理：

保留原请求路径的完整前缀。
示例：

```
nginx
location /back {
    proxy_pass http://backend:5000;
}
```

请求 /back/api/users → 转发到 http://backend:5000/back/api/users
（保留 /back 前缀）

2. proxy_pass http://backend:5000/（带末尾斜杠）

路径处理：
移除匹配的前缀部分，仅转发剩余路径。
示例：

```
nginx
location /back {
    proxy_pass http://backend:5000/;
}
```

请求 /back/api/users → 转发到 http://backend:5000/api/users
（移除 /back 前缀）

# 关于Nginx的配置

```
server {
    listen 80;
    server_name test-front;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理（关键：通过服务名访问后端）
    location /back/ {
        proxy_pass http://test-back:5000/;  # 直接使用后端服务名
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # 解决跨域问题
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS';
        add_header Access-Control-Allow-Headers 'Origin, Content-Type, Accept, Authorization';
    }
}
```
其中

## 1. listen 中监听的端口，此端口为前端服务在docker内的容器端口
## 2. server_name 此项是配置监听的服务名称，填写docker compose中设置的对应的前端服务的名称即可
## 3. 代理的通配URL，此处填写前端请求中代理的通配URL即可，即可将包含有相关的URL的请求转发到指定地址上
## 4. proxy_pass 填写代理的后端地址，使用服务名称和端口号即可

## 其他项目无需专门进行配置，一般跨域都会在后端中进行设置
