import { forwardRef } from "react";

const Input = forwardRef(
  (
    {
      label,
      type = "text",
      placeholder,
      icon,
      className = "",
      ...props
    },
    ref
  ) => {
    return (
      <div className="w-full">
        {label && (
          <label className="mb-2 block text-sm font-medium text-slate-300">
            {label}
          </label>
        )}

        <div
          className={`glass flex h-14 items-center rounded-2xl border border-cyan-500/20 px-4 transition-all duration-300 focus-within:border-cyan-400 focus-within:shadow-[0_0_20px_rgba(34,211,238,.25)] ${className}`}
        >
          {icon && <span className="mr-3 text-cyan-400">{icon}</span>}

          <input
            ref={ref}
            type={type}
            placeholder={placeholder}
            className="h-full w-full bg-transparent text-white placeholder:text-slate-500 outline-none"
            {...props}
          />
        </div>
      </div>
    );
  }
);

Input.displayName = "Input";

export default Input;