"use client"

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { apiClient } from "@/lib/api-client"

export function useSendMessage(chatId: number | null) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (message: { role: string; content: string }) => {
      if (!chatId) throw new Error("Chat ID is required")
      return apiClient.sendMessage(chatId, message)
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["chats", chatId, "messages"],
      })
    },
  })
}
