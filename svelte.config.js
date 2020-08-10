/* this file only to activate IDE svelte config.
 * the main config on rollup setup */
const sveltePreprocess = require("svelte-preprocess");

const defaults = {
  script: "typescript",
  style: "postcss",
};

module.exports = {
  preprocess: sveltePreprocess({ defaults }),
  defaults,
};
