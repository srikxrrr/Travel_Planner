import React from 'react';
import { Compass, Sparkles } from 'lucide-react';

interface HeaderProps {
  onNewTrip: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onNewTrip }) => {
  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3 cursor-pointer" onClick={onNewTrip}>
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-xl">
              <Compass className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">RoamAI</h1>
              <p className="text-xs text-gray-500">AI Travel Planner</p>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center gap-8">
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">How it works</a>
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">Destinations</a>
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">Pricing</a>
            <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              Try Premium
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};