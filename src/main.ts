

// milkdown
import { Crepe } from '@milkdown/crepe';
//import { listener, listenerCtx } from "@milkdown/kit/plugin/listener";
import { insert, replaceAll } from "@milkdown/kit/utils";

import { emoji } from "@milkdown/plugin-emoji";


import '@milkdown/crepe/theme/common/style.css'
import '@milkdown/crepe/theme/frame.css';

// If you need to style tables, you should import this css file.
//import "@milkdown/kit/prose/tables/style/tables.css";
// You should import these predefined prosemirror css styles.
//import "@milkdown/kit/prose/view/style/prosemirror.css";

// Your css file.

import './my-theme.css';



function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}


// 🔗 Get current page URL
const currentUrl = window.location.href;
console.log("Current Page URL:", currentUrl);
const browserUserAgent = window.navigator.userAgent;
console.log("User Agent: ", browserUserAgent);
const isMObileDevice = navigator.maxTouchPoints > 1;
console.log("isMObileDevice: ", isMObileDevice);



// display
var save_controls_node = document.getElementById('save-controls');
if (save_controls_node) {
  if (save_controls_node.style.display === 'none') {
    save_controls_node.style.display = 'flex';
  }
}


const markdown =
  `# Milkdown Editor Crepe
  ### how to use 
 `

const crepe = new Crepe({
  root: '#app',
  defaultValue: markdown,
  features: {
    [Crepe.Feature.Latex]: true,
    [Crepe.Feature.BlockEdit]: true,


  },
  featureConfigs: {

    [Crepe.Feature.CodeMirror]: {

    }

  }
});

// add plugin
crepe.editor.use(emoji);





crepe.create().then(async () => {
  console.log("Editor created");

  // Apply replace and insert actions

  crepe.editor.action(replaceAll("# Choose Milkdown Editor Crepe"));
  crepe.editor.action(insert("\nSome other thing"));
  crepe.editor.action(insert("\nhello " + browserUserAgent + " visit " + currentUrl));
  // Now get updated markdown
  const updatedMd = crepe.getMarkdown();
  console.log("Updated Markdown:", updatedMd);
  await sleep(1);


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


  console.log("btn set");
  // Wait until the DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      // Code to execute after DOM is loaded
      console.log("bth run");
      const filenameInput = document.getElementById('filename-input') as HTMLInputElement;

      const saveBtn = document.getElementById('save-btn');

      if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
          try {

            const filename: string = filenameInput?.value.trim() || "untitled";

            const markdown = crepe.getMarkdown();
            console.log("save \n" + filename + "\n" + markdown);
            const response = await fetch("/md/save", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ markdown, filename }),
            });

            const result = await response.json();
            alert(result.message || "Saved!");
          } catch (err) {
            console.error("Error saving markdown:", err);
            alert("Failed to save.");
          }
        });
      }

    });
  } else {
    // Code to execute immediately (DOM is already loaded)
    console.log("bth run");
    const saveBtn = document.getElementById('save-btn');
    const filenameInput = document.getElementById('filename-input') as HTMLInputElement;

    if (saveBtn) {
      saveBtn.addEventListener('click', async () => {
        try {

          const filename: string = filenameInput?.value.trim() || "untitled";
          const markdown = crepe.getMarkdown();
          console.log("save \n" + markdown);
          const response = await fetch(currentUrl + "/md/save", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ markdown, filename }),
          });

          const result = await response.json();
          alert(result.message || "Saved!");
        } catch (err) {
          console.error("Error saving markdown:", err);
          alert("Failed to save.");
        }
      });
    }

  }





});

console.log("after Editor create");
