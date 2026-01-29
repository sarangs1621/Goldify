import React from 'react';
import { LogOut, Loader2 } from 'lucide-react';

export const LogoutOverlay = () => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full mx-4 animate-in zoom-in-95 duration-300">
        <div className="flex flex-col items-center space-y-6">
          {/* Animated logout icon */}
          <div className="relative">
            <div className="absolute inset-0 bg-primary/20 rounded-full animate-ping"></div>
            <div className="relative bg-primary rounded-full p-6">
              <LogOut className="w-12 h-12 text-white animate-pulse" />
            </div>
          </div>
          
          {/* Message */}
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-semibold text-gray-900">
              You're logging out
            </h2>
            <p className="text-gray-600">
              Please wait a moment...
            </p>
          </div>
          
          {/* Spinner */}
          <div className="flex items-center gap-2 text-primary">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span className="text-sm font-medium">Signing out</span>
          </div>
        </div>
      </div>
    </div>
  );
};