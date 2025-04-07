
// 
//import { createRequire } from 'node:module';
//const require = createRequire(import.meta.url);

// request
//var compose = require('request-compose')
//var Request = compose.Request
//var Response = compose.Response


// milkdown
import { Crepe } from '@milkdown/crepe';
//import { listener, listenerCtx } from "@milkdown/kit/plugin/listener";
import { insert, replaceAll } from "@milkdown/kit/utils";

import { emoji } from "@milkdown/plugin-emoji";


import '@milkdown/crepe/theme/common/style.css'
import '@milkdown/crepe/theme/frame.css';

function sleep(ms:number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}


// 🔗 Get current page URL
const currentUrl = window.location.href;
console.log("Current Page URL:", currentUrl);
const browserUserAgent = window.navigator.userAgent;
console.log("User Agent: ", browserUserAgent );
const isMObileDevice = navigator.maxTouchPoints > 1;
console.log("isMObileDevice: ", isMObileDevice);


const markdown =
  `# Milkdown Editor Crepe
  ### how to use 
 `

const crepe = new Crepe({
  root: '#app',
  defaultValue: markdown,
 features: {
    [Crepe.Feature.Latex]: true,
[Crepe.Feature.BlockEdit]:true,


  },
});

// add plugin
crepe.editor.use(emoji);





crepe.create().then(async  () => { 
  console.log("Editor created");

  // Apply replace and insert actions

  crepe.editor.action(replaceAll("# Choose Milkdown Editor Crepe"));
  crepe.editor.action(insert("\nSome other thing"));
  crepe.editor.action(insert("\nhello " + browserUserAgent + " visit " + currentUrl));
  // Now get updated markdown
  const updatedMd = crepe.getMarkdown();
  console.log("Updated Markdown:", updatedMd);

for(var i = 0 ; i < 100; i++){
  // Now get updated markdown
  const updatedMd = crepe.getMarkdown();
  console.log("Updated Markdown:", updatedMd);
  await sleep(1000); // Wait for one second
}



  //crepe.setReadonly(true);  
  
    // Optional: Live update listener (uncomment to use)
  /*
  crepe.editor.use(listener);
  crepe.editor.config((ctx) => {
    ctx.get(listenerCtx).markdown((_, md) => {
      console.log("Live Markdown Update:", md);
    });
  });
  */
});

console.log("after Editor create");


