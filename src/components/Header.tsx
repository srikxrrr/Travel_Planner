import React from 'react';
import { Plane, Plus, List } from 'lucide-react';

interface HeaderProps {
  activeTab: 'explore' | 'trips';
  onTabChange: (tab: 'explore' | 'trips') => void;
  tripCount: number;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, onTabChange, tripCount }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-xl">
              <Plane className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Travel Planner</h1>
              <p className="text-sm text-gray-600">Plan your perfect getaway</p>
            </div>
          </div>
          
          <nav className="flex items-center gap-1 bg-gray-100 p-1 rounded-lg">
            <button
              onClick={() => onTabChange('explore')}
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                activeTab === 'explore'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Plus className="w-4 h-4" />
              Explore
            </button>
            <button
              onClick={() => onTabChange('trips')}
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                activeTab === 'trips'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <List className="w-4 h-4" />
              My Trips
              {tripCount > 0 && (
                <span className="bg-blue-100 text-blue-600 text-xs px-2 py-0.5 rounded-full">
                  {tripCount}
                </span>
              )}
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};