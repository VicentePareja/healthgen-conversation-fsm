"use client"

import { useChats } from "@/hooks/use-chats"
import { Button } from "@/components/ui/button"
import { PlusCircle } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import { formatDate } from "@/lib/utils"
import { apiClient } from "@/lib/api-client"
import { useQueryClient } from "@tanstack/react-query"

interface SidebarProps {
  onSelectChat: (chatId: number) => void
}

export function Sidebar({ onSelectChat }: SidebarProps) {
  const { data: chats, isLoading, error } = useChats()
  const queryClient = useQueryClient()

  const handleCreateChat = async () => {
    try {
      const newChat = await apiClient.createChat()
      queryClient.invalidateQueries({ queryKey: ["chats"] })
      onSelectChat(newChat.id)
    } catch (error) {
      console.error("Failed to create chat:", error)
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex h-14 items-center border-b px-4">
        <h2 className="text-lg font-semibold">Chats</h2>
      </div>
      <div className="flex-1 overflow-auto p-2">
        {isLoading ? (
          <div className="space-y-2">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex flex-col gap-2 p-2">
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-3 w-1/2" />
              </div>
            ))}
          </div>
        ) : error ? (
          <div className="p-4 text-center text-sm text-muted-foreground">Failed to load chats</div>
        ) : chats?.length === 0 ? (
          <div className="p-4 text-center text-sm text-muted-foreground">No chats yet</div>
        ) : (
          <ul className="space-y-1">
            {chats?.map((chat) => (
              <li key={chat.id}>
                <Button
                  variant="ghost"
                  className="w-full justify-start text-left"
                  onClick={() => onSelectChat(chat.id)}
                >
                  <div className="flex flex-col items-start">
                    <span>Chat #{chat.id}</span>
                    <span className="text-xs text-muted-foreground">{formatDate(chat.created_at)}</span>
                  </div>
                </Button>
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="border-t p-4">
        <Button onClick={handleCreateChat} className="w-full" disabled={isLoading}>
          <PlusCircle className="mr-2 h-4 w-4" />
          New Chat
        </Button>
      </div>
    </div>
  )
}
