# Personal Blog Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a cinematic magazine-style personal blog from the user's Word document, including article list, article detail pages, and extracted images.

**Architecture:** A static React + Vite + TypeScript app stores generated article data in `src/data/articles.ts` and extracted image assets in `public/blog-images`. Navigation is client-side using browser history and slug-based article routes.

**Tech Stack:** React, Vite, TypeScript, Tailwind CSS, Vitest, Word `.docx` XML extraction via Python.

---

## Tasks

- [x] Extract 85 articles from `/Users/fanlongwei/Downloads/个人blog.docx`.
- [x] Extract referenced Word images into `public/blog-images`.
- [x] Generate typed article data in `src/data/articles.ts`.
- [x] Implement cinematic hero, glass navigation, magazine article cards, archive list, and article detail page.
- [x] Add Vitest tests for article count, images, slug lookup, categories, and year range.
- [ ] Run tests, build, and preview locally.
