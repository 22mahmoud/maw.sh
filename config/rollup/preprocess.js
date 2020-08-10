import path from "path";
import sveltePreprocess from "svelte-preprocess";
import hljs from "highlight.js";
import { mdsvex } from "mdsvex";

import * as postcss from "../../postcss.config";

export const preprocess = [
  sveltePreprocess({
    defaults: {
      script: "typescript",
      style: "postcss",
    },
    postcss,
  }),
  mdsvex({
    extension: ".svx",
    layout: path.join(__dirname, "src/components/MdLayout.svelte"),
    highlight: {
      highlighter: (str, lang) => {
        return hljs.highlight(lang, str);
      },
    },
  }),
];
