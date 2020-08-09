import { onwarn } from "./config/rollup/utils";
import { client } from "./config/rollup/client";
import { server } from "./config/rollup/server";
import { serviceworker } from "./config/rollup/serviceworker";

export default {
  client,
  server,
  serviceworker,
};
