import { Response, Request } from "express";

import posts from "./_posts.js";

const contents = JSON.stringify(
  posts.map((post) => {
    return {
      title: post.title,
      slug: post.slug,
    };
  })
);

export function get(_req: Request, res: Response) {
  res.status(200);
  res.json(contents);
}

