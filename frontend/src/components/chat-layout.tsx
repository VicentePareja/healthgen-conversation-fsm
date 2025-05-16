"use client"

import { useState } from "react"
import { Sidebar } from "@/components/sidebar"
import { ChatWindow } from "@/components/chat-window"
import { useMediaQuery } from "@/hooks/use-media-query"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export function ChatLayout() {
  const [selectedChatId, setSelectedChatId] = useState<number | null>(null)
  const isMobile = useMediaQuery("(max-width: 768px)")

  const handleSelectChat = (chatId: number) => {
    setSelectedChatId(chatId)
  }

  if (isMobile) {
    return (
      <div className="flex h-screen flex-col">
        <header className="flex h-14 items-center border-b px-4">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="mr-2">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Toggle menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="p-0">
              <Sidebar onSelectChat={handleSelectChat} />
            </SheetContent>
          </Sheet>
          <h1 className="text-lg font-semibold">HealthGen Chat</h1>
        </header>
        <main className="flex-1">
          <ChatWindow chatId={selectedChatId} />
        </main>
      </div>
    )
  }

  return (
    <div className="flex h-screen">
      <aside className="w-64 border-r">
        <Sidebar onSelectChat={handleSelectChat} />
      </aside>
      <main className="flex-1">
        <ChatWindow chatId={selectedChatId} />
      </main>
    </div>
  )
}
