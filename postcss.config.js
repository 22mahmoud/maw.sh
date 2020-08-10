import cssnano from "cssnano";
import postcssImport from "postcss-import";
import autoprefixer from "autoprefixer";
import postcssPurgecss from "@fullhuman/postcss-purgecss";
import tailwindcss from "tailwindcss";
import * as tailwindcssConfig from "./tailwind.config";

const production = process.env.NODE_ENV === "production";

export const plugins = [
  postcssImport,

  tailwindcss(tailwindcssConfig),

  autoprefixer,

  production &&
    postcssPurgecss({
      content: ["./src/**/*.svelte", "./src/**/*.html"],
      defaultExtractor: (content) =>
        [...content.matchAll(/(?:class:)*([\w\d-/:%.]+)/gm)].map(
          ([_match, group, ..._rest]) => group
        ),
    }),

  production &&
    cssnano({
      preset: ["default", { discardComments: { removeAll: true } }],
    }),
].filter(Boolean);
