import { LoginRequest } from "@/types/auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL!;
console.log(BASE_URL)

async function apiFetch(
    endpoint: string,
    options?: RequestInit
) {
    const response = await fetch(
        `${BASE_URL}${endpoint}`,
        {
            headers: {
                "Content-Type": "application/json",
            },
            ...options,
        },
    );
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.detail || "Login failed");
    }

    return result;
}

export async function loginUser(data: LoginRequest) {
    const response = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify(data),
    });
    return response;
}
