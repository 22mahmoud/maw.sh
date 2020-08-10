import config from "sapper/config/rollup.js";

import { plugins } from "./plugins";
import { onwarn } from "./utils";

export const client = {
  input: config.client.input().replace(/\.js$/, ".ts"),
  output: config.client.output(),
  plugins: [...plugins.shared, ...plugins.client],
  preserveEntrySignatures: false,
  onwarn,
};
