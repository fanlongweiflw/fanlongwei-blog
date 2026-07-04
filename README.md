# Fanlongwei Journal

一个由 Word 博客文档生成的电影感杂志型个人博客。

## 项目内容

- React + Vite + TypeScript
- Tailwind CSS
- Word 文档自动拆分文章数据
- Word 图片自动提取到本地资源
- 首页视频 Hero、文章目录、文章详情页

## 本地启动

```bash
npm install
npm run dev
```

默认访问：

```text
http://localhost:5173/
```

## 测试和构建

```bash
npm test
npm run build
```

## 文章数据

文章数据位于：

```text
src/data/articles.ts
```

图片位于：

```text
public/blog-images/
```

## 从新的 Word 文档更新文章

如果之后有新的 Word 文档，可以运行：

```bash
npm run update:word -- "/path/to/新的个人blog.docx"
```

例如：

```bash
npm run update:word -- "/Users/fanlongwei/Downloads/个人blog.docx"
```

脚本会：

1. 从 Word 中按标题样式拆分文章
2. 提取正文引用的图片到 `public/blog-images/`
3. 重新生成 `src/data/articles.ts`
4. 为每篇文章生成至少 4 个关键词

更新后建议运行：

```bash
npm test
npm run build
```

## 上传 GitHub

第一次上传：

```bash
git init
git add .
git commit -m "feat: create personal blog"
git branch -M main
git remote add origin <你的 GitHub 仓库地址>
git push -u origin main
```

后续更新：

```bash
git add .
git commit -m "chore: update blog content"
git push
```
