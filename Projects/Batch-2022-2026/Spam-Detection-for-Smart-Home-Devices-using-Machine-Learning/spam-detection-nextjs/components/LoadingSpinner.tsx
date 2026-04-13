interface Props {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
}

const sizeMap = { sm: 'h-6 w-6', md: 'h-10 w-10', lg: 'h-16 w-16' };

export default function LoadingSpinner({ size = 'md', label }: Props) {
  return (
    <div className="flex flex-col items-center justify-center gap-3">
      <div
        className={`animate-spin rounded-full border-t-2 border-b-2 border-blue-500 ${sizeMap[size]}`}
      />
      {label && <p className="text-sm text-gray-500">{label}</p>}
    </div>
  );
}
