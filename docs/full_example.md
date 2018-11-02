## Full example

### Dockerfile

```dockerfile
FROM nginx:1.15-alpine AS prod-stage

COPY / /usr/share/nginx/html

RUN echo "server {
  listen 80;
  sendfile on;
  default_type application/octet-stream;
  gzip on;
  gzip_http_version 1.1;
  gzip_disable      "MSIE [1-6]\.";
  gzip_min_length   256;
  gzip_vary         on;
  gzip_proxied      expired no-cache no-store private auth;
  gzip_types        text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript;
  gzip_comp_level   9;
  root /usr/share/nginx/html;
  location / {
    try_files $uri $uri/ /index.html =404;
  }
}" > /etc/nginx/conf.d/default.conf
```

Build and push to docker hub

```bash
docker build -t my/example:1.0.0 .
docker push my/example:1.0.0
```

### Nginx configuration

On your server, Nginx configuration file example :

```nginx
upstream example_up {
    server 127.0.0.1:4210 weight=1 max_fails=1 fail_timeout=5;
    server 127.0.0.1:4220 weight=1 max_fails=1 fail_timeout=5;
}

server {
    listen 80;
    listen [::]:80;

    server_name my.example.com;

    location / {
        proxy_pass http://example_up;
        proxy_set_header Host $host;
    }
}
```

### ZDD configuration

Create the file ~/.config/zdd.json with the following content :

```json
{
  "projects": {
    "example": {
      "active": true,
      "docker_image": "my/example",
      "docker_params": {
        "default": {
          "ports": {
            "80/tcp": 4210
          }
        },
        "instance_2": {
          "ports": {
            "80/tcp": 4220
          }
        }
      }
    }
  }
}
```

### Deployment

```bash
zdd -vvvv example 1.0.0
```
