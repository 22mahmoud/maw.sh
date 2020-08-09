import config from "sapper/config/rollup.js";

import { plugins } from "./plugins";
import { onwarn } from "./utils";

export const serviceworker = {
  input: config.serviceworker.input().replace(/\.js$/, ".ts"),
  output: config.serviceworker.output(),
  plugins: [...plugins.shared, ...plugins.serviceWorker],
  preserveEntrySignatures: false,
  onwarn,
};
