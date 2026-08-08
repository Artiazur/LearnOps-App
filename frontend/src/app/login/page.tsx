"use client";

import { loginUser } from "@/lib/api";
import { useState } from "react";
import Image from "next/image";
import {
  validateEmail,
  validateLoginPassword,
} from "@/lib/validators";
import TextInput from "@/components/TextInput";
import Button from "@/components/ui/Button";
import Card from "@/components/LoginCard";
import { toast } from "sonner";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const handleEmailChange = (
  event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;

    setEmail(value);

    setEmailError(validateEmail(value));
  };

  const handlePasswordChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;

    setPassword(value);

    setPasswordError(validateLoginPassword(value));
  };

  const handleLogin = async () => {
    const emailValidation = validateEmail(email);
    const passwordValidation = validateLoginPassword(password);

    setEmailError(emailValidation);
    setPasswordError(passwordValidation);

    if (emailValidation || passwordValidation) {
      return;
    }

    try {
      const data = await loginUser({
        email,
        password,
      });

      toast.success(`Welcome!`);

    } catch (error) {
        if (error instanceof Error) {
          toast.error(error.message);
        }
      }
  };
  return (
    <main className="min-h-screen bg-background flex items-center justify-center">

      <Card>

        {/* Left Side */}
        <div className="w-[50%] flex items-center justify-center">

          <Image
            src="/images/login-element.png"
            alt="Login Illustration"
            width={600}
            height={455}
            priority
            className="object-contain mt-8"
          />
        </div>

        {/* Right Side */}
        <div className="w-[50%] flex items-center justify-center">

          <div className="w-[280px]">

            <h1
              className="
                text-[72px]
                font-semibold
                text-primary
                text-center
                mb-14
                -translate-x-1
              "
            >
              Login
            </h1>

            <div className="space-y-6 flex flex-col items-center">

              <TextInput
                type="email"
                placeholder="Email"
                value={email}
                onChange={handleEmailChange}
              />

              {emailError && (
                <p className="text-red-600 text-sm">
                  {emailError}
                </p>
              )}

              <TextInput
                type="password"
                placeholder="Password"
                value={password}
                onChange={handlePasswordChange}
              />

              {passwordError && (
                <p className="text-red-600 text-sm">
                  {passwordError}
                </p>
              )}

              <Button
              className="w-55"
              onClick={handleLogin}
              >
              Login
              </Button>

            </div>

          </div>

        </div>

      </Card>

    </main>
  );
}
