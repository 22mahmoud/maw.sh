import { Request, NextFunction, Response } from "express";

import posts from "./_posts";

const lookup = new Map();

posts.forEach((post) => {
  lookup.set(post.slug, post);
});

export function get(req: Request, res: Response, _next: NextFunction) {
  const { slug } = req.params;

  if (lookup.has(slug)) {
    res.status(200);
    res.json(lookup.get(slug));
  } else {
    res.status(404);
    res.json({ message: `Not found` });
  }
}
