'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadDocument } from '../lib/api';
import { Upload, CheckCircle, XCircle, Loader2 } from 'lucide-react';

export default function DocumentUploader() {
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [error, setError] = useState('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setStatus('uploading');
    try {
      for (const file of acceptedFiles) {
        await uploadDocument(file);
      }
      setStatus('success');
      setTimeout(() => setStatus('idle'), 3000);
    } catch (err: any) {
      setStatus('error');
      setError(err.message || 'Failed to upload document');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
  });

  return (
    <div className="p-4 border-b bg-white">
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
  );
}
