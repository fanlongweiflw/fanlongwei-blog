export type ArticleBlock = { type: 'paragraph'; text: string };

export type BlogArticle = {
  id: number;
  slug: string;
  rawTitle: string;
  title: string;
  date: string;
  category: string;
  keywords: string[];
  excerpt: string;
  wordCount: number;
  readingTime: number;
  blocks: ArticleBlock[];
};
