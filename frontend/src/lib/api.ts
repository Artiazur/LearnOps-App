import { LoginRequest } from "@/types/auth";
import {
  getAccessToken,
  setAccessToken,
  clearAccessToken,
} from "./auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL!;

async function refreshAccessToken(): Promise<boolean> {
   /**
   * Request a new access token using the refresh token stored in the
   * HTTP-only cookie.
   *
   * The refresh token is intentionally not accessed directly by the client.
   * If the refresh request fails, the stored access token is cleared and the
   * caller is informed that the authentication session could not be renewed.
   */

  try {
    const response = await fetch(`${BASE_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include", 
    });

    if (!response.ok) {
      clearAccessToken();
      return false;
    }

    const result = await response.json();
    setAccessToken(result.access_token);

    return true;
  } catch {
    clearAccessToken();
    return false;
  }
}

async function apiFetch(
  endpoint: string,
  options?: RequestInit,
  retry = true
) {
  /**
   * Send an authenticated API request and transparently refresh an expired
   * access token when necessary.
   *
   * The current access token is attached to the request when available. If
   * the API responds with 401, the client attempts to obtain a new access
   * token through the refresh flow and retries the original request once.
   *
   * The retry flag prevents an authentication failure from causing an
   * infinite refresh-and-retry loop.
   */

  const token = getAccessToken();

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(token && {
        Authorization: `Bearer ${token}`,
      }),
      ...options?.headers,
    },
  });

  if (response.status === 401 && retry && endpoint !== "/auth/refresh") {
    const refreshed = await refreshAccessToken();

    if (refreshed) {
      return apiFetch(endpoint, options, false);
    }
  }

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Request failed");
  }

  return result;
}

export async function loginUser(data: LoginRequest) {
  /**
   * Authenticate the user and store the access token returned by the API.
   *
   * The refresh token is managed through the HTTP-only cookie set by the
   * backend and is therefore not stored or accessed directly by the client.
   */

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    credentials: "include", 
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Login failed");
  }

  setAccessToken(result.access_token);

  return result;
}

export async function testAuth() {
  /**
   * Verify the current authentication state through the protected API.
   *
   * The request is routed through the shared API wrapper so an expired
   * access token can be refreshed automatically before retrying the request.
   */

  return apiFetch("/auth/test-auth");
}