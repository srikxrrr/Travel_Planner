import React, { useState } from 'react';
import { ArrowLeft, Calendar, Users, DollarSign, Clock, Download, Share2, Heart, Star } from 'lucide-react';
import { TripPlan } from '../App';

interface TripResultsProps {
  tripPlan: TripPlan;
  onNewTrip: () => void;
}

export const TripResults: React.FC<TripResultsProps> = ({ tripPlan, onNewTrip }) => {
  const [activeDay, setActiveDay] = useState(1);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={onNewTrip}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              Plan New Trip
            </button>
            
            <div className="flex items-center gap-3">
              <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                <Heart className="w-4 h-4" />
                Save
              </button>
              <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                <Share2 className="w-4 h-4" />
                Share
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Download className="w-4 h-4" />
                Export PDF
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Your {tripPlan.duration}-Day Trip to {tripPlan.destination}
              </h1>
              <div className="flex items-center gap-6 text-gray-600 mb-4">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>{tripPlan.duration} days</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4" />
                  <span>{tripPlan.travelers} travelers</span>
                </div>
                <div className="flex items-center gap-2">
                  <Star className="w-4 h-4 text-yellow-500" />
                  <span>AI Optimized</span>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2">
                {tripPlan.interests.map(interest => (
                  <span
                    key={interest}
                    className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm"
                  >
                    {interest}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <DollarSign className="w-5 h-5" />
                Estimated Cost
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Accommodation</span>
                  <span className="font-medium">{formatCurrency(tripPlan.estimatedCost.accommodation)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Food & Dining</span>
                  <span className="font-medium">{formatCurrency(tripPlan.estimatedCost.food)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Activities</span>
                  <span className="font-medium">{formatCurrency(tripPlan.estimatedCost.activities)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Transport</span>
                  <span className="font-medium">{formatCurrency(tripPlan.estimatedCost.transport)}</span>
                </div>
                <div className="border-t pt-3 flex justify-between">
                  <span className="font-semibold text-gray-900">Total</span>
                  <span className="font-bold text-xl text-blue-600">{formatCurrency(tripPlan.estimatedCost.total)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Itinerary */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Day Selector */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-24">
              <h3 className="font-semibold text-gray-900 mb-4">Itinerary</h3>
              <div className="space-y-2">
                {tripPlan.itinerary.map(day => (
                  <button
                    key={day.day}
                    onClick={() => setActiveDay(day.day)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      activeDay === day.day
                        ? 'bg-blue-100 text-blue-700 border-2 border-blue-300'
                        : 'hover:bg-gray-50 border-2 border-transparent'
                    }`}
                  >
                    <div className="font-medium">Day {day.day}</div>
                    <div className="text-sm text-gray-600 truncate">{day.title}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Day Details */}
          <div className="lg:col-span-3">
            {tripPlan.itinerary.map(day => (
              activeDay === day.day && (
                <div key={day.day} className="bg-white rounded-2xl shadow-lg p-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="bg-blue-100 text-blue-700 w-10 h-10 rounded-full flex items-center justify-center font-bold">
                      {day.day}
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900">{day.title}</h2>
                      <p className="text-gray-600">Day {day.day} of {tripPlan.duration}</p>
                    </div>
                  </div>

                  <div className="space-y-6">
                    {day.activities.map((activity, index) => (
                      <div key={index} className="flex gap-4 p-4 border border-gray-200 rounded-xl hover:shadow-md transition-shadow">
                        <div className="flex-shrink-0">
                          <div className="bg-gray-100 text-gray-600 w-12 h-12 rounded-lg flex items-center justify-center">
                            <Clock className="w-5 h-5" />
                          </div>
                        </div>
                        <div className="flex-grow">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h4 className="font-semibold text-gray-900">{activity.activity}</h4>
                              <p className="text-sm text-gray-600">{activity.time}</p>
                            </div>
                            {activity.cost && (
                              <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-sm font-medium">
                                {activity.cost}
                              </span>
                            )}
                          </div>
                          <p className="text-gray-700">{activity.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};