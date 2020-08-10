import path from "path";
import resolve from "@rollup/plugin-node-resolve";
import replace from "@rollup/plugin-replace";
import image from "@rollup/plugin-image";
import url from "@rollup/plugin-url";
import json from "@rollup/plugin-json";
import commonjs from "@rollup/plugin-commonjs";
import svelte from "rollup-plugin-svelte";
import babel from "@rollup/plugin-babel";
import typescript from "@rollup/plugin-typescript";
import { terser } from "rollup-plugin-terser";

import { preprocess } from "./preprocess";

const mode = process.env.NODE_ENV;
const dev = mode === "development";
const sourcemap = dev ? "inline" : false;
const legacy = !!process.env.SAPPER_LEGACY_BUILD;

const extensions = [".svelte", ".svx"];

const shared = [
  typescript({ sourceMap: !!sourcemap }),
  commonjs(),
  json(),
  url({
    fileName: "[dirname][hash][extname]",
    sourceDir: path.join(__dirname, "src"),
  }),
];

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
    extensions,
  }),

  resolve({
    browser: true,
    dedupe: ["svelte"],
  }),

  // image(),

  legacy &&
    babel({
      extensions: [".js", ".mjs", ".html", ".svelte", ...extensions],
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
    extensions,
  }),
  resolve({
    dedupe: ["svelte"],
  }),
];

const serviceWorker = [
  resolve(),
  typescript({ sourceMap: !!sourcemap }),
  replace({
    "process.browser": true,
    "process.env.NODE_ENV": JSON.stringify(mode),
  }),
  commonjs(),
  !dev && terser(),
];

export const plugins = {
  shared: shared.filter(Boolean),
  client: client.filter(Boolean),
  server: server.filter(Boolean),
  serviceWorker: serviceWorker.filter(Boolean),
};
