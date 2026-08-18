let accessToken: string | null = null;

export function setAccessToken(token: string) {
    console.log("SETTING ACCESS TOKEN:", token);
    accessToken = token;
}

export function getAccessToken() {
    console.log("GETTING ACCESS TOKEN:", accessToken);
    return accessToken;
}

export function clearAccessToken() {
    accessToken = null;
}