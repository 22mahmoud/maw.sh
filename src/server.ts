import express from "express";
import sirv from "sirv";
import compression from "compression";
import * as sapper from "@sapper/server";

const { PORT, NODE_ENV } = process.env;
const dev = NODE_ENV === "development";

const app = express();

app.use(compression({ threshold: 0 }));

app.use(sirv("static", { dev }));

app.use(sapper.middleware());

app.listen(PORT, (error?: any): void => {
  if (error) console.log("error", error);
});
