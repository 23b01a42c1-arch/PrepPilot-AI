export default function Button({
  children,
  className = "",
  variant = "primary",
  ...props
}) {
  const base =
    "rounded-2xl px-6 py-3 font-semibold transition-all duration-300";

  const styles = {
    primary:
      "bg-cyan-400 text-slate-900 hover:shadow-[0_0_25px_rgba(34,211,238,0.5)] hover:-translate-y-1",

    secondary:
      "border border-cyan-400 text-cyan-300 hover:bg-cyan-400 hover:text-slate-900",
  };

  return (
    <button
      className={`${base} ${styles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}