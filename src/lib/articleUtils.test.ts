import { describe, expect, it } from 'vitest';
import { articles } from '../data/articles';
import { getArticleBySlug, getCategories, getFeaturedArticles, getYearRange } from './articleUtils';

describe('article data generated from Word', () => {
  it('contains the expected number of articles from the Word document', () => {
    expect(articles).toHaveLength(88);
  });

  it('finds articles by slug', () => {
    const first = articles[0];
    expect(getArticleBySlug(first.slug)?.title).toBe(first.title);
  });

  it('returns editorial categories and year range', () => {
    expect(getCategories()).toContain('全部');
    expect(getCategories()).toContain('AI');
    expect(getYearRange()).toBe('2023 — 2026');
  });

  it('selects three non-empty featured articles by default', () => {
    const featured = getFeaturedArticles();
    expect(featured).toHaveLength(3);
    expect(featured.every((article) => article.wordCount > 0)).toBe(true);
  });

  it('adds at least four core keywords to every article', () => {
    expect(articles.every((article) => article.keywords.length >= 4)).toBe(true);
    expect(getArticleBySlug('2025-02-20-大模型是如何训练的')?.keywords).toContain('大模型');
  });
});
