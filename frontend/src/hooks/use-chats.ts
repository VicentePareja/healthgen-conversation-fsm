"use client"

import { useQuery } from "@tanstack/react-query"
import { apiClient } from "@/lib/api-client"

export function useChats() {
  return useQuery({
    queryKey: ["chats"],
    queryFn: () => apiClient.getChats(),
  })
}
