import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import { MessageBubble } from "@/components/message-bubble"
import type { Message } from "@/lib/types"

describe("MessageBubble", () => {
  it("should render user message correctly", () => {
    const userMessage: Message = {
      id: 1,
      chat_id: 1,
      role: "user",
      content: "Hello, how are you?",
      timestamp: "2023-01-01T12:00:00Z",
    }

    render(<MessageBubble message={userMessage} />)

    expect(screen.getByText("Hello, how are you?")).toBeInTheDocument()

    // Check if the message is aligned to the right (user message)
    const messageContainer = screen.getByText("Hello, how are you?").closest("div")
    expect(messageContainer?.parentElement).toHaveClass("justify-end")
  })

  it("should render assistant message correctly", () => {
    const assistantMessage: Message = {
      id: 2,
      chat_id: 1,
      role: "assistant",
      content: "I'm doing well, thank you!",
      timestamp: "2023-01-01T12:01:00Z",
    }

    render(<MessageBubble message={assistantMessage} />)

    expect(screen.getByText("I'm doing well, thank you!")).toBeInTheDocument()

    // Check if the message is aligned to the left (assistant message)
    const messageContainer = screen.getByText("I'm doing well, thank you!").closest("div")
    expect(messageContainer?.parentElement).toHaveClass("justify-start")
  })
})
