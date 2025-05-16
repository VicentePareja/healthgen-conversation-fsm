import { describe, it, expect, vi, beforeEach } from "vitest"
import { renderHook, waitFor } from "@testing-library/react"
import { useChats } from "@/hooks/use-chats"
import { apiClient } from "@/lib/api-client"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import type { ReactNode } from "react"

// Mock the API client
vi.mock("@/lib/api-client", () => ({
  apiClient: {
    getChats: vi.fn(),
  },
}))

// Create a wrapper for the query client
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  })

  return ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe("useChats", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should fetch chats successfully", async () => {
    const mockChats = [
      { id: 1, created_at: "2023-01-01T00:00:00Z" },
      { id: 2, created_at: "2023-01-02T00:00:00Z" },
    ]

    vi.mocked(apiClient.getChats).mockResolvedValue(mockChats)

    const { result } = renderHook(() => useChats(), {
      wrapper: createWrapper(),
    })

    // Initially loading
    expect(result.current.isLoading).toBe(true)

    // Wait for the query to resolve
    await waitFor(() => expect(result.current.isLoading).toBe(false))

    // Check if data is correct
    expect(result.current.data).toEqual(mockChats)
    expect(apiClient.getChats).toHaveBeenCalledTimes(1)
  })

  it("should handle error when fetching chats fails", async () => {
    const error = new Error("Failed to fetch chats")
    vi.mocked(apiClient.getChats).mockRejectedValue(error)

    const { result } = renderHook(() => useChats(), {
      wrapper: createWrapper(),
    })

    // Wait for the query to resolve
    await waitFor(() => expect(result.current.isLoading).toBe(false))

    // Check if error is handled
    expect(result.current.error).toBeDefined()
    expect(result.current.error?.message).toBe("Failed to fetch chats")
  })
})
