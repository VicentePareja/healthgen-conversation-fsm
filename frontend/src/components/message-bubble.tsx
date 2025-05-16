import type { Message } from "@/lib/types"
import { cn, formatDate } from "@/lib/utils"

interface MessageBubbleProps {
  message: Message
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user"

  return (
    <div className={cn("mb-4 flex", isUser ? "justify-end" : "justify-start")}>
      <div
        className={cn(
          "max-w-[80%] rounded-lg px-4 py-2",
          isUser ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground",
        )}
      >
        <div className="whitespace-pre-wrap break-words">{message.content}</div>
        <div className={cn("mt-1 text-right text-xs", isUser ? "text-primary-foreground/70" : "text-muted-foreground")}>
          {formatDate(message.timestamp)}
        </div>
      </div>
    </div>
  )
}
