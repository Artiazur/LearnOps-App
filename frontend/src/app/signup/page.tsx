"use client";
import { useState } from "react";
import Image from "next/image";

import {
  validateEmail,
  validatePassword,
  validateFirstName,
  validateLastName,
  validateConfirmPassword,
} from "@/lib/validators";
import TextInput from "@/components/TextInput";
import Button from "@/components/ui/Button";
import Card from "@/components/SignUpCard";

export default function LoginPage() {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [firstNameError, setFirstNameError] = useState("");
    const [lastNameError, setLastNameError] = useState("");
    const [emailError, setEmailError] = useState("");
    const [passwordError, setPasswordError] = useState("");
    const [confirmPasswordError, setConfirmPasswordError] = useState("");

    const handleFirstNameChange = (
  event: React.ChangeEvent<HTMLInputElement>
) => {
    const value = event.target.value;

    setFirstName(value);
    setFirstNameError(validateFirstName(value));
    };

    const handleLastNameChange = (
    event: React.ChangeEvent<HTMLInputElement>
    ) => {
    const value = event.target.value;

    setLastName(value);
    setLastNameError(validateLastName(value));
    };

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

    setPasswordError(validatePassword(value));

    if (confirmPassword) {
        setConfirmPasswordError(
        validateConfirmPassword(value, confirmPassword)
        );
    }
    };

    const handleConfirmPasswordChange = (
    event: React.ChangeEvent<HTMLInputElement>
    ) => {
    const value = event.target.value;

    setConfirmPassword(value);

    setConfirmPasswordError(
        validateConfirmPassword(password, value)
    );
    };
    const handleSignUp = () => {
    const firstNameValidation = validateFirstName(firstName);
    const lastNameValidation = validateLastName(lastName);
    const emailValidation = validateEmail(email);
    const passwordValidation = validatePassword(password);
    const confirmPasswordValidation =
        validateConfirmPassword(password, confirmPassword);

    setFirstNameError(firstNameValidation);
    setLastNameError(lastNameValidation);
    setEmailError(emailValidation);
    setPasswordError(passwordValidation);
    setConfirmPasswordError(confirmPasswordValidation);

    if (
        firstNameValidation ||
        lastNameValidation ||
        emailValidation ||
        passwordValidation ||
        confirmPasswordValidation
    ) {
        return;
    }

    console.log("Everything is valid.");
    };
    return (
    <main className="min-h-screen bg-background flex items-center justify-center">

        <Card>

            {/* Background Image */}
            <div className="absolute inset-0 flex items-center justify-center">
                <Image
                src="/images/login-element.png"
                alt="Background Illustration"
                width={900}
                height={850}
                priority
                className="
                    object-contain
                    opacity-12
                    pointer-events-none
                    select-none
                "
                />
            </div>
            {/* Form */}
            <div className="absolute inset-0 flex items-center justify-center z-10">
                <div className="w-[340px]">

                    <h1
                        className="
                        text-[72px]
                        font-semibold
                        text-primary
                        text-center
                        mb-12
                        "
                    >
                        Sign Up
                    </h1>

                    <div className="space-y-5">

                        <TextInput
                        type="text"
                        placeholder="First Name"
                        value={firstName}
                        onChange={handleFirstNameChange}
                        />

                        {firstNameError && (
                        <p className="text-red-600 text-sm">
                            {firstNameError}
                        </p>
                        )}
                        <TextInput
                        type="text"
                        placeholder="Last Name"
                        value={lastName}
                        onChange={handleLastNameChange}
                        />

                        {lastNameError && (
                        <p className="text-red-600 text-sm">
                            {lastNameError}
                        </p>
                        )}
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
                        <TextInput
                        type="password"
                        placeholder="Confirm Password"
                        value={confirmPassword}
                        onChange={handleConfirmPasswordChange}
                        />

                        {confirmPasswordError && (
                        <p className="text-red-600 text-sm">
                            {confirmPasswordError}
                        </p>
                        )}

                        <Button
                        className="w-72 mx-auto block mt-4"
                        onClick={handleSignUp}
                        >
                        Create Account
                        </Button>

                    </div>

                </div>

            </div>

        </Card>

    </main>
  );
}