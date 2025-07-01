import React from 'react';
import { MapPin, DollarSign, Calendar, Star } from 'lucide-react';
import { Destination } from '../types';

interface DestinationCardProps {
  destination: Destination;
  onSelect: (destination: Destination) => void;
}

export const DestinationCard: React.FC<DestinationCardProps> = ({ destination, onSelect }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
      <div className="relative h-48 overflow-hidden">
        <img
          src={destination.imageUrl}
          alt={destination.name}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
        />
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1">
          <Star className="w-4 h-4 text-yellow-500 fill-current" />
          <span className="text-sm font-medium">4.8</span>
        </div>
      </div>
      
      <div className="p-6">
        <div className="flex items-center gap-2 mb-2">
          <MapPin className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">{destination.country}</span>
        </div>
        
        <h3 className="text-xl font-bold text-gray-900 mb-2">{destination.name}</h3>
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">{destination.description}</p>
        
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-1">
            <DollarSign className="w-4 h-4 text-green-600" />
            <span className="text-lg font-semibold text-green-600">
              ${destination.estimatedCost.toLocaleString()}
            </span>
          </div>
          
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4 text-blue-600" />
            <span className="text-xs text-blue-600">{destination.bestTimeToVisit}</span>
          </div>
        </div>
        
        <div className="mb-4">
          <div className="flex flex-wrap gap-1">
            {destination.activities.slice(0, 3).map((activity, index) => (
              <span
                key={index}
                className="bg-blue-50 text-blue-700 px-2 py-1 rounded-full text-xs"
              >
                {activity}
              </span>
            ))}
            {destination.activities.length > 3 && (
              <span className="text-xs text-gray-500">+{destination.activities.length - 3} more</span>
            )}
          </div>
        </div>
        
        <button
          onClick={() => onSelect(destination)}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 px-4 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
        >
          Plan Trip
        </button>
      </div>
    </div>
  );
};