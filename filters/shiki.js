#!/usr/bin/env node
// @ts-check

"use strict";

import pandoc from "pandoc-filter";
import { getHighlighter } from "shiki";
import fs from "node:fs";

function logToFile(message) {
  fs.appendFileSync("debug.log", message + "\n", "utf8");
}

async function highlightCodeBlock(code, lang) {
  const highlighter = await getHighlighter({
    themes: ["vitesse-dark"],
    langs: [lang],
  });

  const html = highlighter.codeToHtml(code, {
    lang,
    theme: "vitesse-dark",
  });

  return html;
}

pandoc.stdio(async ({ t: type, c: value }) => {
  if (type === "CodeBlock") {
    const [[_, [lang]], code] = value;
    const highlighted = await highlightCodeBlock(code, lang);
    return pandoc.RawBlock("html", highlighted);
  }
});
