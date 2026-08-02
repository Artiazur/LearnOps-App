export default function LoginCard({ children }) {
  return (
    <div
      className="
        bg-card
        w-[1300px]
        h-[720px]
        rounded-[48px]
        shadow-xl
        flex
        overflow-hidden
        px-3
      "
    >
      {children}
    </div>
  );
}