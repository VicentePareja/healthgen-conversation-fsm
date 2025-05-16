import type { Chat, Message } from "@/lib/types"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`)
    }

    return response.json()
  }

  async getChats(): Promise<Chat[]> {
    return this.request<Chat[]>("/chats/")
  }

  async createChat(): Promise<Chat> {
    return this.request<Chat>("/chats/", {
      method: "POST",
    })
  }

  async getChatMessages(chatId: number): Promise<Message[]> {
    return this.request<Message[]>(`/chats/${chatId}/messages/`)
  }

  async sendMessage(chatId: number, message: { role: string; content: string }): Promise<Message> {
    return this.request<Message>(`/chats/${chatId}/messages/`, {
      method: "POST",
      body: JSON.stringify(message),
    })
  }
}

export const apiClient = new ApiClient(API_URL)
