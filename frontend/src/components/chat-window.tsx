"use client"

import { useState } from "react"
import { useChatMessages } from "@/hooks/use-chat-messages"
import { useSendMessage } from "@/hooks/use-send-message"
import { MessageList } from "@/components/message-list"
import { MessageInput } from "@/components/message-input"
import type { Message } from "@/lib/types"

interface ChatWindowProps {
  chatId: number | null
}

export function ChatWindow({ chatId }: ChatWindowProps) {
  const [optimisticMessages, setOptimisticMessages] = useState<Message[]>([])

  const {
    data: messages,
    isLoading,
    error,
  } = useChatMessages(chatId, {
    enabled: !!chatId,
  })

  const { mutate: sendMessage, isPending } = useSendMessage(chatId)

  const handleSendMessage = (content: string) => {
    if (!chatId) return

    // Create optimistic user message
    const optimisticUserMessage: Message = {
      id: Date.now(),
      chat_id: chatId,
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    }

    setOptimisticMessages((prev) => [...prev, optimisticUserMessage])

    // Send message to API
    sendMessage(
      { role: "user", content },
      {
        onSuccess: (assistantMessage) => {
          // Clear optimistic messages once we get real data
          setOptimisticMessages([])
        },
        onError: () => {
          // Remove optimistic message on error
          setOptimisticMessages((prev) => prev.filter((msg) => msg.id !== optimisticUserMessage.id))
        },
      },
    )
  }

  // Combine server messages with optimistic messages
  const allMessages = [...(messages || []), ...optimisticMessages]

  if (!chatId) {
    return (
      <div className="flex h-full flex-col items-center justify-center p-4 text-center">
        <h2 className="mb-2 text-xl font-semibold">Welcome to HealthGen Chat</h2>
        <p className="mb-4 text-muted-foreground">Select a chat from the sidebar or create a new one to get started</p>
      </div>
    )
  }

  return (
    <div className="chat-container flex flex-col">
      <div className="flex h-14 items-center border-b px-4">
        <h2 className="text-lg font-semibold">Chat #{chatId}</h2>
      </div>
      <MessageList messages={allMessages} isLoading={isLoading} error={error} />
      <div className="border-t p-4">
        <MessageInput onSendMessage={handleSendMessage} isLoading={isPending} disabled={!chatId} />
      </div>
    </div>
  )
}
