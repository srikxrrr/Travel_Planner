import React from 'react';
import { Calendar, Users, DollarSign, MapPin, Clock } from 'lucide-react';
import { Trip } from '../types';
import { format, differenceInDays } from 'date-fns';

interface TripCardProps {
  trip: Trip;
  onEdit?: (trip: Trip) => void;
  onDelete?: (tripId: string) => void;
}

export const TripCard: React.FC<TripCardProps> = ({ trip, onEdit, onDelete }) => {
  const duration = differenceInDays(trip.endDate, trip.startDate) + 1;
  
  const getStatusColor = (status: Trip['status']) => {
    switch (status) {
      case 'planned':
        return 'bg-yellow-100 text-yellow-800';
      case 'booked':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300">
      <div className="relative h-32 overflow-hidden">
        <img
          src={trip.destination.imageUrl}
          alt={trip.destination.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute top-3 right-3">
          <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${getStatusColor(trip.status)}`}>
            {trip.status}
          </span>
        </div>
      </div>
      
      <div className="p-4">
        <div className="flex items-center gap-2 mb-2">
          <MapPin className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">{trip.destination.country}</span>
        </div>
        
        <h3 className="text-lg font-bold text-gray-900 mb-3">{trip.destination.name}</h3>
        
        <div className="space-y-2 mb-4">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Calendar className="w-4 h-4" />
            <span>
              {format(trip.startDate, 'MMM dd')} - {format(trip.endDate, 'MMM dd, yyyy')}
            </span>
          </div>
          
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Clock className="w-4 h-4" />
            <span>{duration} day{duration > 1 ? 's' : ''}</span>
          </div>
          
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Users className="w-4 h-4" />
            <span>{trip.travelers} traveler{trip.travelers > 1 ? 's' : ''}</span>
          </div>
          
          <div className="flex items-center gap-2 text-sm">
            <DollarSign className="w-4 h-4 text-green-600" />
            <span className="font-semibold text-green-600">
              ${trip.budget.toLocaleString()}
            </span>
          </div>
        </div>
        
        {trip.notes && (
          <p className="text-sm text-gray-600 mb-4 line-clamp-2">{trip.notes}</p>
        )}
        
        <div className="flex gap-2">
          {onEdit && (
            <button
              onClick={() => onEdit(trip)}
              className="flex-1 px-3 py-2 text-sm border border-blue-300 text-blue-700 rounded-lg hover:bg-blue-50 transition-colors"
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(trip.id)}
              className="flex-1 px-3 py-2 text-sm border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors"
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
};