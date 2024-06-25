#!/usr/bin/env node
// @ts-check

"use strict";

import pandoc from "pandoc-filter";
import { getHighlighter } from "shiki";

/**
 * @param {string} code
 * @param {string} lang
 * @returns {Promise<string>}
 */
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
  if (type === "CodeBlock" || type === "Code") {
    const [[_, [lang]], code] = value;
    const highlighted = await highlightCodeBlock(code, lang);

    return type === "CodeBlock"
      ? pandoc.RawBlock("html", highlighted)
      : pandoc.RawInline("html", highlighted);
  }
});
