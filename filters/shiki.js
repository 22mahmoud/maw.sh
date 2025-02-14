#!/usr/bin/env node

import { transformerNotationWordHighlight } from '@shikijs/transformers';
import pandoc from 'pandoc-filter';
import { codeToHtml } from 'shiki';

/**
 * @param {string} code
 * @param {string} lang
 * @returns {Promise<string>}
 */
function highlightCodeBlock(code, lang) {
  return codeToHtml(code, {
    lang,
    theme: 'vitesse-dark',
    transformers: [transformerNotationWordHighlight({ matchAlgorithm: 'v3' })],
  });
}

pandoc.stdio(async ({ t: type, c: value }) => {
  if (type === 'CodeBlock') {
    const [[_, meta], code] = value;
    const lang = meta?.[0] || '';
    const highlighted = await highlightCodeBlock(code, lang);
    return pandoc.RawBlock('html', highlighted);
  }
});
