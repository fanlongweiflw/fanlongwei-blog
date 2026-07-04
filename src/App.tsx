import { useEffect, useState } from 'react';
import { ArticlePage } from './components/ArticlePage';
import { HomePage } from './components/HomePage';
import { Navigation } from './components/Navigation';

type ActiveSection = 'home' | 'archive';

function getSlugFromPath() {
  const match = window.location.pathname.match(/^\/article\/([^/]+)/);
  return match ? decodeURIComponent(match[1]) : null;
}

export default function App() {
  const [slug, setSlug] = useState<string | null>(() => getSlugFromPath());
  const [activeSection, setActiveSection] = useState<ActiveSection>('home');

  useEffect(() => {
    const onPopState = () => setSlug(getSlugFromPath());
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  useEffect(() => {
    const onScroll = () => {
      if (getSlugFromPath()) return;

      const archiveTop = document.getElementById('archive')?.getBoundingClientRect().top ?? Number.POSITIVE_INFINITY;

      if (archiveTop <= 160) {
        setActiveSection('archive');
      } else {
        setActiveSection('home');
      }
    };

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, [slug]);

  const openArticle = (nextSlug: string) => {
    window.history.pushState({}, '', `/article/${encodeURIComponent(nextSlug)}`);
    setSlug(nextSlug);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const goHome = () => {
    window.history.pushState({}, '', '/');
    setSlug(null);
    setActiveSection('home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const goArchive = () => {
    window.history.pushState({}, '', '/');
    setSlug(null);
    setActiveSection('archive');
    window.setTimeout(() => document.getElementById('archive')?.scrollIntoView({ behavior: 'smooth' }), 60);
  };

  const returnToArticleList = (articleSlug: string) => {
    window.history.pushState({}, '', '/');
    setSlug(null);
    window.setTimeout(() => {
      document.getElementById(`article-row-${articleSlug}`)?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }, 80);
  };

  return (
    <>
      <Navigation activeSection={activeSection} onHome={goHome} onArchive={goArchive} />
      {slug ? <ArticlePage slug={slug} goHome={() => returnToArticleList(slug)} /> : <HomePage openArticle={openArticle} />}
    </>
  );
}
