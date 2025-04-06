
import { Crepe } from '@milkdown/crepe';
import { listener, listenerCtx } from "@milkdown/kit/plugin/listener";
import { insert, replaceAll } from "@milkdown/kit/utils";
import '@milkdown/crepe/theme/common/style.css'
import '@milkdown/crepe/theme/frame.css';

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}


// 🔗 Get current page URL
const currentUrl = window.location.href;
console.log("Current Page URL:", currentUrl);



const markdown =
  `# Milkdown Editor Crepe
  ### how to use 
 `

const crepe = new Crepe({
  root: '#app',
  defaultValue: markdown,
 features: {
    [Crepe.Feature.Latex]: true,
  },
});
 

await crepe.create().then(() => { 
  console.log("Editor created");

  // Apply replace and insert actions

  crepe.editor.action(replaceAll("# Choose Milkdown Editor Crepe"));
  crepe.editor.action(insert("\nSome other thing"));
  crepe.editor.action(insert(currentUrl));
  // Now get updated markdown
  const updatedMd = crepe.getMarkdown();
  console.log("Updated Markdown:", updatedMd);
  
  
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


for(var i = 0 ; i < 100; i++){
  // Now get updated markdown
  const updatedMd = crepe.getMarkdown();
  console.log("Updated Markdown:", updatedMd);
  await sleep(1000); // Wait for one second
}
