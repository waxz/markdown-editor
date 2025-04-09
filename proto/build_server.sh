#!/bin/bash
# https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-l>
SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to re>
done
DIR=$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)

export PATH=$PATH:$DIR/protobuf-javascript/bin:$DIR/protoc/bin

PROTO_DIR=./src/server/proto

mkdir -p ${PROTO_DIR}
# Generate JavaScript code
npx grpc_tools_node_protoc \
  --js_out=import_style=commonjs,binary:${PROTO_DIR} \
  --grpc_out=grpc_js:${PROTO_DIR} \
  --plugin=protoc-gen-grpc=./node_modules/.bin/grpc_tools_node_protoc_plugin \
  -I ./proto \
  proto/*.proto

# Generate TypeScript code (d.ts)
npx grpc_tools_node_protoc \
  --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
  --ts_out=grpc_js:${PROTO_DIR} \
  -I ./proto \
  proto/*.proto

#flask-protobuf
protoc \
  --python_out=./api \
  -I ./proto \
  proto/*.proto
