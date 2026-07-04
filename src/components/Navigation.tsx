type ActiveSection = 'home' | 'archive';

type NavigationProps = {
  activeSection: ActiveSection;
  onHome: () => void;
  onArchive: () => void;
};

export function Navigation({ activeSection, onHome, onArchive }: NavigationProps) {
  const linkClass = (section: ActiveSection) =>
    section === activeSection
      ? 'text-sm text-white transition-colors'
      : 'text-sm text-white/60 transition-colors hover:text-white';

  return (
    <nav className="fixed inset-x-0 top-0 z-40 px-5 py-5 text-white">
      <div className="relative mx-auto flex max-w-7xl items-center justify-between rounded-full px-5 py-3 md:px-7 liquid-glass">
        <button onClick={onHome} className="font-display text-3xl tracking-tight">
          Fanlongwei<sup className="text-xs">®</sup>
        </button>
        <div className="absolute left-1/2 hidden -translate-x-1/2 items-center gap-8 md:flex">
          <button onClick={onHome} className={linkClass('home')}>首页</button>
          <button onClick={onArchive} className={linkClass('archive')}>全部文章</button>
        </div>
        <button onClick={onArchive} className="rounded-full px-5 py-2 text-sm transition-transform hover:scale-[1.03] liquid-glass">
          开始阅读
        </button>
      </div>
    </nav>
  );
}
