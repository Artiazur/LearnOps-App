"use client";

import { Eye, EyeOff } from "lucide-react";
import { useState } from "react";

export default function TextInput({
  type = "text",
  placeholder,
  value,
  onChange,
}) {
  const [showPassword, setShowPassword] = useState(false);

  const inputType =
    type === "password"
      ? (showPassword ? "text" : "password")
      : type;

  return (
    <div className="relative w-full">

      <input
        type={inputType}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="
          w-full
          rounded-2xl
          bg-input
          text-base
          placeholder:text-[#151f36]
          px-3
          py-5
          pr-12
          outline-none
          border
          border-transparent
          focus:border-primary
          transition
        "
      />

      {type === "password" && (
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="
            absolute
            right-4
            top-1/2
            -translate-y-1/2
            text-primary/60
            hover:text-primary
            transition
          "
        >
          {showPassword ? (
            <EyeOff size={20} />
          ) : (
            <Eye size={20} />
          )}
        </button>
      )}

    </div>
  );
}