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

PROTO_DIR=./src/client/proto

mkdir -p ${PROTO_DIR}

# Generate Types
npx proto-loader-gen-types --longs=String --enums=String --defaults --oneofs --grpcLib=@grpc/grpc-js --outDir=${PROTO_DIR} proto/*.proto

# Generate JS and TS code
protoc -I=./proto ./proto/*.proto \
  --proto_path="$DIR/protoc/include" \
  --js_out=import_style=commonjs:${PROTO_DIR} \
  --grpc-web_out=import_style=typescript,mode=grpcwebtext:${PROTO_DIR}
# PROTO_DIR=./src/grpc/proto
# mkdir -p ${PROTO_DIR}

# protoc -I=./proto ./proto/*.proto \
#   --proto_path="$DIR/protoc/include" \
#   --js_out=import_style=typescript:${PROTO_DIR} \
#   --grpc-web_out=import_style=typescript,mode=grpcwebtext:${PROTO_DIR}


 
