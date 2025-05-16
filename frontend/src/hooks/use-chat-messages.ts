"use client"

import { useQuery } from "@tanstack/react-query"
import { apiClient } from "@/lib/api-client"
import type { UseQueryOptions } from "@tanstack/react-query"
import type { Message } from "@/lib/types"

export function useChatMessages(
  chatId: number | null,
  options?: Omit<UseQueryOptions<Message[], Error>, "queryKey" | "queryFn">,
) {
  return useQuery({
    queryKey: ["chats", chatId, "messages"],
    queryFn: () => {
      if (!chatId) throw new Error("Chat ID is required")
      return apiClient.getChatMessages(chatId)
    },
    ...options,
  })
}
