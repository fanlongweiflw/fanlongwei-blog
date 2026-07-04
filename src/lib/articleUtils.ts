import { articles } from '../data/articles';
import type { BlogArticle } from './types';

export function getArticleBySlug(slug: string): BlogArticle | undefined {
  return articles.find((article) => article.slug === slug);
}

export function getFeaturedArticles(limit = 3): BlogArticle[] {
  return articles.filter((article) => article.wordCount > 0).slice(0, limit);
}

export function getArticlesByCategory(category: string): BlogArticle[] {
  if (category === '全部') return articles;
  return articles.filter((article) => article.category === category);
}

export function getCategories(): string[] {
  return ['全部', ...Array.from(new Set(articles.map((article) => article.category)))];
}

export function getYearRange(): string {
  const years = articles
    .map((article) => article.date.slice(0, 4))
    .filter((year) => /^\d{4}$/.test(year));
  return `${Math.min(...years.map(Number))} — ${Math.max(...years.map(Number))}`;
}
