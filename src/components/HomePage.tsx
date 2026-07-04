import { articles } from '../data/articles';
import { getYearRange } from '../lib/articleUtils';
import type { BlogArticle } from '../lib/types';
import { Hero } from './Hero';

type HomePageProps = { openArticle: (slug: string) => void };

export function HomePage({ openArticle }: HomePageProps) {
  return (
    <>
      <Hero
        onRead={() => document.getElementById('archive')?.scrollIntoView({ behavior: 'smooth' })}
        stats={[
          { value: `${articles.length}`, label: '篇文章' },
          { value: getYearRange(), label: '写作时间' },
        ]}
      />
      <main className="bg-[#061014] text-[#f7f1e8]">
        <section id="archive" className="mx-auto max-w-7xl px-6 py-20">
          <div className="mb-8 border-b border-white/10 pb-6">
            <p className="text-sm uppercase tracking-[0.35em] text-[#b7a98f]">Archive</p>
          </div>
          <div className="divide-y divide-white/10">
            {articles.map((article) => <ArticleRow key={article.slug} article={article} openArticle={openArticle} />)}
          </div>
        </section>
      </main>
    </>
  );
}

function ArticleRow({ article, openArticle }: { article: BlogArticle; openArticle: (slug: string) => void }) {
  return (
    <button id={`article-row-${article.slug}`} onClick={() => openArticle(article.slug)} className="group grid w-full scroll-mt-28 gap-5 py-7 text-left transition md:grid-cols-[130px_1fr_120px] md:items-center">
      <div className="text-sm text-white/40">{article.date}</div>
      <div>
        <div className="mb-3 flex flex-wrap items-center gap-2 text-xs text-[#b7a98f]">
          {article.keywords.map((keyword) => (
            <span key={keyword} className="rounded-full border border-[#b7a98f]/25 px-2.5 py-1 text-[#d8c7a5]/80">
              {keyword}
            </span>
          ))}
        </div>
        <h3 className="font-display text-3xl leading-tight text-white transition group-hover:text-[#ead8b7]">{article.title}</h3>
        <p className="mt-2 line-clamp-2 text-sm leading-6 text-white/45">{article.excerpt}</p>
      </div>
      <div className="text-sm text-white/35 md:text-right">{article.wordCount} 字<br />{article.readingTime} 分钟</div>
    </button>
  );
}
