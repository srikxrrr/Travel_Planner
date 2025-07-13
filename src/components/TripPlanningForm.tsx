import React, { useState } from 'react';
import { MapPin, Calendar, Users, DollarSign, Heart, Loader2, Sparkles } from 'lucide-react';
import { TripPlan } from '../App';

interface TripPlanningFormProps {
  onTripGenerated: (tripPlan: TripPlan) => void;
  isGenerating: boolean;
  setIsGenerating: (generating: boolean) => void;
}

export const TripPlanningForm: React.FC<TripPlanningFormProps> = ({
  onTripGenerated,
  isGenerating,
  setIsGenerating
}) => {
  const [destination, setDestination] = useState('');
  const [duration, setDuration] = useState(3);
  const [travelers, setTravelers] = useState(2);
  const [budget, setBudget] = useState('moderate');
  const [interests, setInterests] = useState<string[]>([]);

  const interestOptions = [
    'Culture & History',
    'Food & Dining',
    'Adventure',
    'Nature & Parks',
    'Shopping',
    'Nightlife',
    'Museums',
    'Architecture',
    'Beaches',
    'Photography'
  ];

  const toggleInterest = (interest: string) => {
    setInterests(prev => 
      prev.includes(interest) 
        ? prev.filter(i => i !== interest)
        : [...prev, interest]
    );
  };

  const generateMockItinerary = (dest: string, days: number): TripPlan => {
    const activities = [
      { time: '9:00 AM', activity: 'Visit Historic District', description: 'Explore the charming old town with guided tour', cost: '$25' },
      { time: '12:00 PM', activity: 'Local Cuisine Lunch', description: 'Try authentic local dishes at recommended restaurant', cost: '$35' },
      { time: '2:30 PM', activity: 'Museum Visit', description: 'Discover local art and culture', cost: '$15' },
      { time: '5:00 PM', activity: 'Scenic Viewpoint', description: 'Watch sunset from the best vantage point', cost: 'Free' },
      { time: '7:30 PM', activity: 'Traditional Dinner', description: 'Fine dining experience with local specialties', cost: '$65' }
    ];

    const itinerary = Array.from({ length: days }, (_, i) => ({
      day: i + 1,
      title: i === 0 ? 'Arrival & City Exploration' : 
             i === days - 1 ? 'Final Adventures & Departure' : 
             `Discover ${dest} - Day ${i + 1}`,
      activities: activities.slice(0, Math.floor(Math.random() * 3) + 3)
    }));

    return {
      id: `trip_${Date.now()}`,
      destination: dest,
      duration: days,
      travelers,
      budget,
      interests,
      itinerary,
      estimatedCost: {
        accommodation: days * 120,
        food: days * 80,
        activities: days * 60,
        transport: 200,
        total: days * 260 + 200
      }
    };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!destination.trim()) return;

    setIsGenerating(true);
    
    // Simulate AI processing time
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const tripPlan = generateMockItinerary(destination, duration);
    onTripGenerated(tripPlan);
    setIsGenerating(false);
  };

  return (
    <div className="bg-white rounded-3xl shadow-2xl p-8 border border-gray-100">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Plan Your Next Adventure</h2>
        <p className="text-gray-600">Fill in the details and let AI create your perfect itinerary</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <MapPin className="w-4 h-4 inline mr-2" />
              Where do you want to go?
            </label>
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              placeholder="e.g., Paris, Tokyo, Bali..."
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Calendar className="w-4 h-4 inline mr-2" />
              How many days?
            </label>
            <select
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            >
              {[1,2,3,4,5,6,7,8,9,10,14,21].map(day => (
                <option key={day} value={day}>{day} day{day > 1 ? 's' : ''}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Users className="w-4 h-4 inline mr-2" />
              Number of travelers
            </label>
            <select
              value={travelers}
              onChange={(e) => setTravelers(Number(e.target.value))}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            >
              {[1,2,3,4,5,6,7,8].map(num => (
                <option key={num} value={num}>{num} traveler{num > 1 ? 's' : ''}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <DollarSign className="w-4 h-4 inline mr-2" />
              Budget preference
            </label>
            <select
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            >
              <option value="budget">Budget-friendly</option>
              <option value="moderate">Moderate</option>
              <option value="luxury">Luxury</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            <Heart className="w-4 h-4 inline mr-2" />
            What are you interested in? (Select all that apply)
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
            {interestOptions.map(interest => (
              <button
                key={interest}
                type="button"
                onClick={() => toggleInterest(interest)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  interests.includes(interest)
                    ? 'bg-blue-100 text-blue-700 border-2 border-blue-300'
                    : 'bg-gray-50 text-gray-700 border-2 border-transparent hover:bg-gray-100'
                }`}
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={isGenerating || !destination.trim()}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Creating your perfect trip...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Generate My Trip Plan
            </>
          )}
        </button>
      </form>

      {isGenerating && (
        <div className="mt-6 text-center">
          <div className="inline-flex items-center gap-2 text-gray-600">
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <span className="ml-2">AI is crafting your personalized itinerary...</span>
          </div>
        </div>
      )}
    </div>
  );
};