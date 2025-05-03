# Milkdown Examples: Editor Crepe

A example for using crepe editor, which is a markdown editor based on Milkdown.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/Milkdown/examples/tree/main/editor-crepe)

## Getting Started


```bash
pnpm install  && pnpm start --host 0.0.0.0 --port 8005 --base mdeditor
```

or

```bash
./run_editor.sh

```

# generate html
```
docker run --name quartz_builder -v /tmp/quartz:/tmp/quartz -v ./content:/tmp/content -v ./quartz-dist:/tmp/output -w /tmp/quartz --rm  node:22 bash -c "npm install -g npm@11.2.0 && npm i && npx quartz build -d /tmp/content -o /tmp/output"
```

