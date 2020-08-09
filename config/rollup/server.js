import config from "sapper/config/rollup.js";

import { plugins } from "./plugins";
import { onwarn } from "./utils";
import pkg from "../../package.json";

const mode = process.env.NODE_ENV;
const dev = mode === "development";
const sourcemap = dev ? "inline" : false;

export const server = {
  input: { server: config.server.input().server.replace(/\.js$/, ".ts") },
  output: { ...config.server.output(), sourcemap },
  plugins: [...plugins.shared, ...plugins.server],
  external: Object.keys(pkg.dependencies).concat(
    require("module").builtinModules
  ),

  preserveEntrySignatures: "strict",
  onwarn,
};
