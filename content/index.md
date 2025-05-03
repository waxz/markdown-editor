---
title: Welcome to Quartz
---

This is a blank Quartz installation.
See the [documentation](https://quartz.jzhao.xyz) for how to get started.

---

##### self host
```bash
sudo npm i npm@11.2.0 -g

git clone git@github.com:waxz/quartz.git
cd quartz
```

#### start server 
```bash
export QUARTZ_PORT=8003
export QUARTZ_CONTENT=./content/

npm i
npx quartz build --serve --watch --port $QUARTZ_PORT  -d $QUARTZ_CONTENT
```

#### start server with nginx
```bash
export QUARTZ_PORT=8003
export QUARTZ_CONTENT=./content/
export QUARTZ_DOMAIN=quartz-public
export QUARTZ_USER=quartz
export QUARTZ_PSW=quartz
./run_quartz.sh
```
