'use client';

import React, { useCallback, useEffect, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { getDocuments, api } from '../lib/api';
import { Upload, CheckCircle, XCircle, Loader2, FileText } from 'lucide-react';
export default function DocumentUploader({ sessionId }: { sessionId: string }) {
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [error, setError] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState<{filename: string, id: string}[]>([]);

  const fetchDocuments = useCallback(async () => {
    try {
      const data = await getDocuments(sessionId);
      setUploadedFiles(data);
    } catch (err) {
      console.error('Failed to fetch documents', err);
    }
  }, [sessionId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchDocuments();
  }, [fetchDocuments]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setStatus('uploading');
    try {
      for (const file of acceptedFiles) {
        const formData = new FormData();
        formData.append('file', file);
        // We need to pass session_id to the upload API
        await api.post(`/documents/upload?session_id=${sessionId}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      await fetchDocuments();
      setStatus('success');
      setTimeout(() => setStatus('idle'), 2000);
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'Failed to upload document');
      setTimeout(() => setStatus('idle'), 5000);
    }
  }, [sessionId, fetchDocuments]);


  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
  });

  return (
    <div className="flex flex-col gap-4">
      <div className="p-4 border rounded-xl bg-white shadow-sm">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors cursor-pointer ${
            isDragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-slate-300'
          }`}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center">
            {status === 'idle' && (
              <>
                <Upload className="text-slate-400 mb-2" size={24} />
                <p className="text-sm text-slate-600 font-medium">Click or drag documents here</p>
                <p className="text-xs text-slate-400">PDF, DOCX, TXT</p>
              </>
            )}
            {status === 'uploading' && (
              <>
                <Loader2 className="animate-spin text-blue-600 mb-2" size={24} />
                <p className="text-sm text-blue-600 font-medium">Indexing documents...</p>
              </>
            )}
            {status === 'success' && (
              <>
                <CheckCircle className="text-green-500 mb-2" size={24} />
                <p className="text-sm text-green-500 font-medium">Done!</p>
              </>
            )}
            {status === 'error' && (
              <>
                <XCircle className="text-red-500 mb-2" size={24} />
                <p className="text-sm text-red-500 font-medium">Error</p>
                <p className="text-xs text-red-400">{error}</p>
              </>
            )}
          </div>
        </div>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="px-1">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Indexed Documents</h3>
            <span className="text-[10px] bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded-full font-bold">{uploadedFiles.length}</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {uploadedFiles.map((file, idx) => (
              <div key={idx} className="flex items-center gap-2 bg-white border px-3 py-1.5 rounded-lg text-xs text-slate-600 shadow-sm transition-all hover:border-blue-200">
                <FileText size={14} className="text-blue-500" />
                <span className="font-medium">{file.filename}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
