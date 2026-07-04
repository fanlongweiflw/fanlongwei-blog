import { ArrowLeft } from 'lucide-react';
import { getArticleBySlug } from '../lib/articleUtils';

type ArticlePageProps = { slug: string; goHome: () => void };

export function ArticlePage({ slug, goHome }: ArticlePageProps) {
  const article = getArticleBySlug(slug);

  if (!article) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#061014] px-6 text-[#f7f1e8]">
        <div className="text-center">
          <h1 className="font-display text-5xl">文章没有找到</h1>
          <button onClick={goHome} className="mt-8 rounded-full px-6 py-3 liquid-glass">返回目录页</button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#061014] text-[#f7f1e8]">
      <article>
        <header className="relative overflow-hidden px-6 pb-14 pt-36">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(234,216,183,0.18),transparent_34%),linear-gradient(180deg,#0b1c23,#061014)]" />
          <div className="relative mx-auto max-w-4xl">
            <button onClick={goHome} className="mb-12 inline-flex items-center gap-2 text-sm text-white/55 transition hover:text-white"><ArrowLeft size={16} /> 返回目录页</button>
            <div className="mb-5 flex flex-wrap gap-3 text-sm text-[#b7a98f]">
              <span>{article.date}</span><span>·</span><span>{article.readingTime} 分钟阅读</span>
            </div>
            <h1 className="font-display text-5xl leading-none tracking-[-1.5px] text-white md:text-7xl">{article.title}</h1>
          </div>
        </header>

        <div className="mx-auto max-w-3xl px-6 pb-28">
          {article.blocks.length === 0 ? (
            <p className="rounded-[1.5rem] border border-white/10 bg-white/[0.04] p-8 text-white/55">这篇文章还没有正文内容，后续可以继续从 Word 中补充。</p>
          ) : (
            <div className="article-content">
              {article.blocks.map((block, index) => <p key={index}>{block.text}</p>)}
            </div>
          )}
        </div>
      </article>
    </main>
  );
}
