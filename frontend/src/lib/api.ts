const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface RequestOptions extends RequestInit {
    retries?: number;
    retryDelay?: number;
}

async function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function fetchWithRetry<T>(
    endpoint: string,
    options: RequestOptions = {}
): Promise<T> {
    const { retries = 3, retryDelay = 1000, ...fetchOptions } = options;

    let lastError: any;

    for (let i = 0; i < retries; i++) {
        try {
            const res = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...fetchOptions,
                headers: {
                    "Content-Type": "application/json",
                    ...fetchOptions.headers,
                },
                cache: "no-store", // Ensure server component fetches fresh data
            });

            if (!res.ok) {
                throw new Error(`API Error: ${res.status} ${res.statusText}`);
            }

            return (await res.json()) as T;
        } catch (error) {
            lastError = error;
            console.warn(`Attempt ${i + 1} failed for ${endpoint}:`, error);
            if (i < retries - 1) await sleep(retryDelay);
        }
    }

    throw lastError;
}
