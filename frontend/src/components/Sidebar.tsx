'use client'

import { Conversation } from '@/types'

interface SidebarProps {
  conversations: Conversation[]
  activeConversation: string | null
  onNewChat: () => void
  onSelectConversation: (id: string) => void
  onDeleteConversation: (id: string) => void
  selectedModel: string
  onModelChange: (model: string) => void
}

const models = ['NLP Hukum v1', 'NLP Hukum v2 (Coming Soon)']

export default function Sidebar({
  conversations,
  activeConversation,
  onNewChat,
  onSelectConversation,
  onDeleteConversation,
  selectedModel,
  onModelChange,
}: SidebarProps) {
  return (
    <div className="w-64 bg-[#171717] flex flex-col h-full">
      <div className="p-3">
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg border border-[#424242] hover:bg-[#2f2f2f] transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span className="text-sm">Chat Baru</span>
        </button>
      </div>

      <div className="px-3 pb-3">
        <label className="text-xs text-[#9b9b9b] mb-1 block">Model</label>
        <select
          value={selectedModel}
          onChange={(e) => onModelChange(e.target.value)}
          className="w-full bg-[#2f2f2f] border border-[#424242] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#666]"
        >
          {models.map((model) => (
            <option key={model} value={model} disabled={model.includes('Coming Soon')}>
              {model}
            </option>
          ))}
        </select>
      </div>

      <div className="flex-1 overflow-y-auto scrollbar-hide px-2">
        <div className="text-xs text-[#9b9b9b] px-2 py-2">Riwayat Chat</div>
        {conversations.length === 0 ? (
          <div className="text-xs text-[#666] px-2 py-4 text-center">
            Belum ada percakapan
          </div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`group flex items-center gap-2 px-2 py-2 rounded-lg cursor-pointer mb-1 ${
                activeConversation === conv.id
                  ? 'bg-[#2f2f2f]'
                  : 'hover:bg-[#212121]'
              }`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <svg className="w-4 h-4 text-[#9b9b9b] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span className="text-sm truncate flex-1">{conv.title}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  onDeleteConversation(conv.id)
                }}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-[#424242] rounded transition-opacity"
              >
                <svg className="w-3 h-3 text-[#9b9b9b]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          ))
        )}
      </div>

      <div className="p-3 border-t border-[#424242]">
        <div className="flex items-center gap-2 px-2 py-2 text-sm text-[#9b9b9b]">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>NLP Hukum AI</span>
        </div>
      </div>
    </div>
  )
}
