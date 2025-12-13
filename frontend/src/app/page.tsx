'use client'

import { useState, useRef, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import ChatArea from '@/components/ChatArea'
import { Message, Conversation } from '@/types'

export default function Home() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversation, setActiveConversation] = useState<string | null>(null)
  const [selectedModel, setSelectedModel] = useState('NLP Hukum v1')

  const currentConversation = conversations.find(c => c.id === activeConversation)

  const createNewChat = () => {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: 'Chat Baru',
      messages: [],
      createdAt: new Date(),
    }
    setConversations(prev => [newConversation, ...prev])
    setActiveConversation(newConversation.id)
  }

  const addMessage = (conversationId: string, message: Message) => {
    setConversations(prev =>
      prev.map(conv => {
        if (conv.id === conversationId) {
          const updatedMessages = [...conv.messages, message]
          const title = conv.messages.length === 0 && message.role === 'user' 
            ? message.content.slice(0, 30) + (message.content.length > 30 ? '...' : '')
            : conv.title
          return { ...conv, messages: updatedMessages, title }
        }
        return conv
      })
    )
  }

  const deleteConversation = (id: string) => {
    setConversations(prev => prev.filter(c => c.id !== id))
    if (activeConversation === id) {
      setActiveConversation(null)
    }
  }

  return (
    <div className="flex h-screen">
      <Sidebar
        conversations={conversations}
        activeConversation={activeConversation}
        onNewChat={createNewChat}
        onSelectConversation={setActiveConversation}
        onDeleteConversation={deleteConversation}
        selectedModel={selectedModel}
        onModelChange={setSelectedModel}
      />
      <ChatArea
        conversation={currentConversation}
        onSendMessage={(message) => {
          if (activeConversation) {
            addMessage(activeConversation, message)
          }
        }}
        addMessage={addMessage}
        selectedModel={selectedModel}
      />
    </div>
  )
}
