import { Request, Response } from "express";

import { getPosts } from "../../utils/posts";

export async function get(_req: Request, res: Response) {
  res.status(200).json(getPosts());
}
