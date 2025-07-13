import React from 'react';
import { Sparkles, MapPin, Clock, Users } from 'lucide-react';

export const Hero: React.FC = () => {
  return (
    <div className="bg-gradient-to-br from-blue-50 via-white to-purple-50 pt-16 pb-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
          <Sparkles className="w-4 h-4" />
          AI-Powered Trip Planning
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
          Plan your perfect trip
          <br />
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            in seconds
          </span>
        </h1>
        
        <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
          Tell us where you want to go, and our AI will create a personalized itinerary 
          with the best places to visit, eat, and stay.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto mb-16">
          <div className="flex flex-col items-center">
            <div className="bg-blue-100 p-4 rounded-2xl mb-4">
              <MapPin className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Choose Destination</h3>
            <p className="text-gray-600 text-sm">Tell us where you want to explore</p>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="bg-purple-100 p-4 rounded-2xl mb-4">
              <Clock className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Set Preferences</h3>
            <p className="text-gray-600 text-sm">Duration, budget, and interests</p>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="bg-green-100 p-4 rounded-2xl mb-4">
              <Users className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Get Your Plan</h3>
            <p className="text-gray-600 text-sm">Receive a detailed itinerary instantly</p>
          </div>
        </div>
      </div>
    </div>
  );
};