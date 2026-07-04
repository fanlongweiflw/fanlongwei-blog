import { ArrowDown } from 'lucide-react';

type HeroStat = { value: string; label: string };

type HeroProps = { onRead: () => void; stats: HeroStat[] };

export function Hero({ onRead, stats }: HeroProps) {
  return (
    <section className="relative min-h-screen overflow-hidden bg-[#00314a] text-white">
      <video
        className="absolute inset-0 z-0 h-full w-full object-cover"
        autoPlay
        loop
        muted
        playsInline
        src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4"
      />
      <div className="absolute inset-0 z-[1] bg-black/10" />
      <div className="relative z-10 mx-auto flex min-h-screen max-w-7xl flex-col items-center justify-center px-6 pb-24 pt-36 text-center">
        <h1 className="animate-fade-rise max-w-6xl font-display text-5xl font-normal leading-[0.95] tracking-[-2.46px] sm:text-7xl md:text-8xl">
          判断，比答案更重要
        </h1>
        <p className="animate-fade-rise-delay mt-8 max-w-2xl text-base leading-relaxed text-white/68 sm:text-lg">
          记录我对 AI 产品、用户需求、创作工具与工作实践的观察和思考
        </p>
        <div className="animate-fade-rise-delay-2 mt-6 flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-xs text-white/24">
          {stats.map((stat) => (
            <div key={stat.label} className="inline-flex items-baseline gap-1.5">
              <span className="text-sm font-medium leading-none text-white/42 md:text-base">{stat.value}</span>
              <span className="text-[10px] tracking-[0.14em] text-white/18">{stat.label}</span>
            </div>
          ))}
        </div>
        <button
          onClick={onRead}
          className="animate-fade-rise-delay-2 mt-12 inline-flex cursor-pointer items-center gap-3 rounded-full px-12 py-5 text-base text-white transition-transform hover:scale-[1.03] liquid-glass"
        >
          开始阅读 <ArrowDown size={18} />
        </button>
      </div>
    </section>
  );
}
