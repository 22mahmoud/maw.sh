import { Response, Request } from "express";

import posts from "./_posts";

const contents = posts.map((post) => {
  return {
    title: post.title,
    slug: post.slug,
  };
});

export function get(_req: Request, res: Response) {
  res.status(200);
  res.json(contents);
}
