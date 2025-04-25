npm install -g npm@11.3.0 && npm install -g pnpm && pnpm install

./proto/build_client.sh
./proto/build_server.sh

npm run build
