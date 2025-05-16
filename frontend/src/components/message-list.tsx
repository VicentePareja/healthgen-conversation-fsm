"use client"

import { useEffect, useRef } from "react"
import type { Message } from "@/lib/types"
import { MessageBubble } from "@/components/message-bubble"
import { Skeleton } from "@/components/ui/skeleton"

interface MessageListProps {
  messages: Message[] | undefined
  isLoading: boolean
  error: Error | null
}

export function MessageList({ messages, isLoading, error }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  return (
    <div className="message-list flex-1 overflow-y-auto p-4">
      {isLoading ? (
        <div className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className={`flex ${i % 2 === 0 ? "justify-start" : "justify-end"}`}>
              <div className={`max-w-[80%] rounded-lg p-1`}>
                <Skeleton className="h-16 w-64" />
              </div>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="flex h-full items-center justify-center">
          <p className="text-destructive">Error loading messages. Please try again.</p>
        </div>
      ) : messages?.length === 0 ? (
        <div className="flex h-full items-center justify-center">
          <p className="text-muted-foreground">No messages yet. Start the conversation!</p>
        </div>
      ) : (
        <>
          {messages?.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  )
}
