export interface Chat {
  id: number
  created_at: string
}

export interface Message {
  id: number
  chat_id: number
  role: string
  content: string
  timestamp: string
}
