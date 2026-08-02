export default function Button({
  children,
  onClick,
  className = "",
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`
        py-4
        rounded-2xl
        bg-primary
        text-white
        font-semibold
        cursor-pointer
        transition
        hover:opacity-90
        active:scale-[0.98]
        text-m
        ${className}
      `}
    >
      {children}
    </button>
  );
}