import sveltePreprocess from "svelte-preprocess";
import resolve from "@rollup/plugin-node-resolve";
import replace from "@rollup/plugin-replace";
import commonjs from "@rollup/plugin-commonjs";
import svelte from "rollup-plugin-svelte";
import babel from "@rollup/plugin-babel";
import typescript from "@rollup/plugin-typescript";
import { terser } from "rollup-plugin-terser";

import * as postcss from "../../postcss.config";

const mode = process.env.NODE_ENV;
const dev = mode === "development";
const sourcemap = dev ? "inline" : false;
const legacy = !!process.env.SAPPER_LEGACY_BUILD;

const preprocess = [
  sveltePreprocess({
    defaults: {
      script: "typescript",
    },
    postcss,
  }),
  // You could have more preprocessors, like MDsveX
];

const shared = [typescript({ sourceMap: !!sourcemap }), commonjs()];

const client = [
  replace({
    "process.browser": true,
    "process.env.NODE_ENV": JSON.stringify(mode),
  }),
  svelte({
    dev,
    hydratable: true,
    emitCss: true,
    preprocess,
  }),
  resolve({
    browser: true,
    dedupe: ["svelte"],
  }),

  legacy &&
    babel({
      extensions: [".js", ".mjs", ".html", ".svelte"],
      babelHelpers: "runtime",
      exclude: ["node_modules/@babel/**"],
    }),

  !dev &&
    terser({
      module: true,
    }),
];

const server = [
  replace({
    "process.browser": false,
    "process.env.NODE_ENV": JSON.stringify(mode),
  }),
  svelte({
    generate: "ssr",
    dev,
    preprocess,
  }),
  resolve({
    dedupe: ["svelte"],
  }),
];

const serviceWorker = [
  resolve(),
  replace({
    "process.browser": true,
    "process.env.NODE_ENV": JSON.stringify(mode),
  }),
  !dev && terser(),
];

export const plugins = {
  shared,
  client,
  serviceWorker,
  server,
};
