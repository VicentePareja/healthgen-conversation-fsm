"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"

type MessageType = {
  id: string
  content: string
  sender: "user" | "bot"
  options?: string[]
}

export default function ChatbotPage() {
  const [messages, setMessages] = useState<MessageType[]>([
    {
      id: "1",
      content: "Welcome to the HealthCare Scheduler. Are you looking to schedule an influenza vaccination?",
      sender: "bot",
      options: ["Yes", "No"],
    },
  ])
  const [input, setInput] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    const userMessage: MessageType = {
      id: Date.now().toString(),
      content: input,
      sender: "user",
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")

    // Simulate bot response (in a real app, this would call your FSM logic)
    setTimeout(() => {
      simulateBotResponse(input)
    }, 1000)
  }

  const handleOptionClick = (option: string) => {
    // Add user's selected option as a message
    const userMessage: MessageType = {
      id: Date.now().toString(),
      content: option,
      sender: "user",
    }

    setMessages((prev) => [...prev, userMessage])

    // Simulate bot response based on option
    setTimeout(() => {
      simulateBotResponse(option)
    }, 1000)
  }

  const simulateBotResponse = (userInput: string) => {
    // This is a simple mock of responses - in the real implementation,
    // this would be replaced with your FSM logic
    let botResponse: MessageType

    const lowercaseInput = userInput.toLowerCase()

    if (lowercaseInput.includes("yes") && messages.length <= 2) {
      botResponse = {
        id: Date.now().toString(),
        content: "Great! Can I have your name, please?",
        sender: "bot",
      }
    } else if (messages.length === 4) {
      botResponse = {
        id: Date.now().toString(),
        content: "Thanks! Are you above 18 years old?",
        sender: "bot",
        options: ["Yes", "No"],
      }
    } else if (lowercaseInput.includes("yes") && messages.length === 6) {
      botResponse = {
        id: Date.now().toString(),
        content: "Here are the available slots. Which one do you prefer?",
        sender: "bot",
        options: ["Tomorrow at 10 AM", "Tomorrow at 3 PM", "Friday at 2 PM", "Monday at 11 AM"],
      }
    } else if (messages.length === 8) {
      botResponse = {
        id: Date.now().toString(),
        content: `Your appointment is scheduled for ${userInput}. Do you need another service?`,
        sender: "bot",
        options: ["Yes", "No"],
      }
    } else if (lowercaseInput.includes("no") && messages.length >= 9) {
      botResponse = {
        id: Date.now().toString(),
        content: "Thank you for using the HealthCare Scheduler. Goodbye!",
        sender: "bot",
      }
    } else {
      botResponse = {
        id: Date.now().toString(),
        content: "I'm sorry, I didn't understand that. Could you please try again?",
        sender: "bot",
      }
    }

    setMessages((prev) => [...prev, botResponse])
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <Card className="w-full max-w-md h-[600px] flex flex-col shadow-lg">
        <div className="bg-blue-600 text-white p-4 rounded-t-lg">
          <h1 className="text-xl font-bold">Healthcare Scheduler</h1>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.sender === "user"
                    ? "bg-blue-600 text-white rounded-tr-none"
                    : "bg-gray-200 text-gray-800 rounded-tl-none"
                }`}
              >
                <p>{message.content}</p>

                {message.options && (
                  <div className="mt-2 space-y-2">
                    {message.options.map((option) => (
                      <Button
                        key={option}
                        variant="outline"
                        className={`w-full justify-start ${
                          message.sender === "user"
                            ? "bg-blue-700 hover:bg-blue-800 text-white border-blue-500"
                            : "bg-white hover:bg-gray-100 text-gray-800 border-gray-300"
                        }`}
                        onClick={() => handleOptionClick(option)}
                      >
                        {option}
                      </Button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 border-t">
          <form onSubmit={handleSendMessage} className="flex space-x-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1"
            />
            <Button type="submit" size="icon">
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  )
}
