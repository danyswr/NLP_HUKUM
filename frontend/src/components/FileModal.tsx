'use client'

import { GDriveFile } from '@/types'

interface FileModalProps {
  file: GDriveFile | null
  isOpen: boolean
  onClose: () => void
}

export default function FileModal({ file, isOpen, onClose }: FileModalProps) {
  if (!isOpen || !file) return null

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  const getDownloadUrl = (url: string) => {
    return url
  }

  return (
    <div 
      className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-[#2f2f2f] rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden shadow-2xl">
        <div className="flex items-center justify-between p-4 border-b border-[#424242]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                <path d="M14 2v6h6"/>
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-white truncate max-w-[400px]">{file.filename}</h3>
              <p className="text-xs text-[#9b9b9b]">Dokumen PDF</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-[#424242] rounded-lg transition-colors"
          >
            <svg className="w-5 h-5 text-[#9b9b9b]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="p-4">
          <div className="mb-4">
            <h4 className="text-sm font-medium text-[#9b9b9b] mb-2">Preview Dokumen</h4>
            <div className="bg-[#212121] rounded-lg p-4 max-h-[300px] overflow-y-auto">
              <p className="text-sm text-[#e0e0e0] whitespace-pre-wrap leading-relaxed">
                {file.preview || "Preview tidak tersedia. Klik tombol di bawah untuk membuka dokumen lengkap di Google Drive."}
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <a
              href={file.gdrive_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg transition-colors font-medium"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              Buka di Google Drive
            </a>
            <a
              href={getDownloadUrl(file.gdrive_url)}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white py-3 px-4 rounded-lg transition-colors font-medium"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
