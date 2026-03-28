// ============================================
// Loading Skeleton Component
// ============================================
// Placeholder while content loads

export function SkeletonProductCard() {
  return (
    <div className="glass-dark animate-pulse">
      <div className="h-48 bg-slate-700 rounded-t-2xl"></div>
      <div className="p-4 space-y-3">
        <div className="h-4 bg-slate-700 rounded w-3/4"></div>
        <div className="h-4 bg-slate-700 rounded"></div>
        <div className="h-4 bg-slate-700 rounded w-1/2"></div>
      </div>
    </div>
  );
}

export function SkeletonGrid({ count = 12 }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {Array(count).fill(0).map((_, i) => (
        <SkeletonProductCard key={i} />
      ))}
    </div>
  );
}

// Default export for convenience
export default SkeletonGrid;
