import * as React from "react"
import { cn } from "@/app/lib/utils"

export function Card(props: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("bg-white rounded-2xl shadow p-4", props.className)} {...props} />
  )
}