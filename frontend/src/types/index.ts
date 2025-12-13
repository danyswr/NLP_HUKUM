export interface GDriveFile {
  filename: string
  gdrive_url: string
  gdrive_id: string
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  files?: GDriveFile[]
  folderUrl?: string
  timestamp: Date
}

export interface Conversation {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
}

export interface ChatResponse {
  reply: string
  files: GDriveFile[]
  folder_url?: string
}
