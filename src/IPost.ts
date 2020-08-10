export interface IPostMeta {
  title: string;
  auto: string;
  description: string;
  categories?: string[];
  keywords?: string[];
  slug: string;
  date?: string;
}

export interface IPost {
  content: string;
  meta: IPostMeta;
}
