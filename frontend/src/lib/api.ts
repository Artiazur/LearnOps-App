import { LoginRequest } from "@/types/auth";
import { getAccessToken, setAccessToken } from "./auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL!;

async function apiFetch(
    endpoint: string,
    options?: RequestInit
) {
    const token = getAccessToken();

    console.log("ACCESS TOKEN:", token);

    const response = await fetch(
        `${BASE_URL}${endpoint}`,
        {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(token && {
                    Authorization: `Bearer ${token}`,
                }),
                ...options?.headers,
            },
        },
    );

    console.log(
        "REQUEST:",
        endpoint,
        "TOKEN:",
        token
    );

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.detail || "Request failed");
    }

    return result;
}

export async function loginUser(data: LoginRequest) {
    const result = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify(data),
    });

    setAccessToken(result.access_token);

    return result;
}

export async function testAuth() {
  return apiFetch("/auth/test-auth");
}