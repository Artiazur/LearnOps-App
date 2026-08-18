"use client";

import { testAuth } from "@/lib/api";
import { useState } from "react";

export default function TestAuthPage() {
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleTestAuth = async () => {
        try {
            setError("");

            const result = await testAuth();

            setMessage(
                `${result.message} User ID: ${result.user_id}`
            );
        } catch (error) {
            setMessage("");

            if (error instanceof Error) {
                setError(error.message);
            } else {
                setError("Something went wrong.");
            }
        }
    };

    return (
        <main className="min-h-screen flex items-center justify-center">
            <div className="flex flex-col items-center gap-4">
                <button
                    onClick={handleTestAuth}
                    className="px-4 py-2 rounded"
                >
                    Test Authentication
                </button>

                {message && (
                    <p>{message}</p>
                )}

                {error && (
                    <p className="text-red-600">
                        {error}
                    </p>
                )}
            </div>
        </main>
    );
}