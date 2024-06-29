#!/usr/bin/env node
// @ts-check

"use strict";

import pandoc from "pandoc-filter";
import { codeToHtml } from "shiki";
import { transformerNotationWordHighlight } from "@shikijs/transformers";

/**
 * @param {string} code
 * @param {string} lang
 * @returns {Promise<string>}
 */
function highlightCodeBlock(code, lang) {
  return codeToHtml(code, {
    lang,
    theme: "vitesse-black",
    transformers: [transformerNotationWordHighlight()],
  });
}

pandoc.stdio(async ({ t: type, c: value }) => {
  if (type === "CodeBlock") {
    const [[_, [lang]], code] = value;
    const highlighted = await highlightCodeBlock(code, lang);

    return type === "CodeBlock"
      ? pandoc.RawBlock("html", highlighted)
      : pandoc.RawInline("html", highlighted);
  }
});
