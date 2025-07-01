import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { DestinationCard } from './components/DestinationCard';
import { TripPlanningModal } from './components/TripPlanningModal';
import { TripCard } from './components/TripCard';
import { destinations } from './data/destinations';
import { Destination, Trip } from './types';
import { Search, Filter, MapPin } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState<'explore' | 'trips'>('explore');
  const [selectedDestination, setSelectedDestination] = useState<Destination | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [trips, setTrips] = useState<Trip[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCountry, setSelectedCountry] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load trips from localStorage on component mount
  useEffect(() => {
    try {
      setIsLoading(true);
      const savedTrips = localStorage.getItem('travelPlannerTrips');
      if (savedTrips) {
        const parsedTrips = JSON.parse(savedTrips);
        
        // Validate and convert trip data
        const validTrips = parsedTrips
          .filter((trip: any) => {
            // Basic validation
            return trip && 
                   trip.id && 
                   trip.destination && 
                   trip.startDate && 
                   trip.endDate &&
                   trip.budget &&
                   trip.travelers;
          })
          .map((trip: any) => ({
            ...trip,
            startDate: new Date(trip.startDate),
            endDate: new Date(trip.endDate),
            budget: Number(trip.budget),
            travelers: Number(trip.travelers),
            notes: trip.notes || '',
            status: trip.status || 'planned'
          }));
        
        setTrips(validTrips);
      }
    } catch (err) {
      console.error('Error loading trips from localStorage:', err);
      setError('Failed to load saved trips');
      // Clear corrupted data
      localStorage.removeItem('travelPlannerTrips');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Save trips to localStorage whenever trips change
  useEffect(() => {
    if (!isLoading) {
      try {
        localStorage.setItem('travelPlannerTrips', JSON.stringify(trips));
      } catch (err) {
        console.error('Error saving trips to localStorage:', err);
        setError('Failed to save trips');
      }
    }
  }, [trips, isLoading]);

  const handleDestinationSelect = (destination: Destination) => {
    setSelectedDestination(destination);
    setIsModalOpen(true);
  };

  const handleTripSave = (tripData: Omit<Trip, 'id'>) => {
    try {
      const newTrip: Trip = {
        ...tripData,
        id: `trip_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      };
      
      setTrips(prev => [...prev, newTrip]);
      setActiveTab('trips');
      setError(null);
    } catch (err) {
      console.error('Error saving trip:', err);
      setError('Failed to save trip');
    }
  };

  const handleTripDelete = (tripId: string) => {
    try {
      setTrips(prev => prev.filter(trip => trip.id !== tripId));
      setError(null);
    } catch (err) {
      console.error('Error deleting trip:', err);
      setError('Failed to delete trip');
    }
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedDestination(null);
  };

  const filteredDestinations = destinations.filter(destination => {
    const matchesSearch = destination.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         destination.country.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         destination.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCountry = !selectedCountry || destination.country === selectedCountry;
    return matchesSearch && matchesCountry;
  });

  const countries = [...new Set(destinations.map(d => d.country))].sort();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your travel plans...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        activeTab={activeTab} 
        onTabChange={setActiveTab} 
        tripCount={trips.length}
      />

      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
              <div className="ml-auto pl-3">
                <button
                  onClick={() => setError(null)}
                  className="text-red-400 hover:text-red-600"
                >
                  <span className="sr-only">Dismiss</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'explore' ? (
          <div>
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Discover Amazing Destinations</h2>
              <p className="text-gray-600">Find your next adventure from our curated collection of destinations</p>
            </div>

            {/* Search and Filter */}
            <div className="mb-8 flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search destinations..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <select
                  value={selectedCountry}
                  onChange={(e) => setSelectedCountry(e.target.value)}
                  className="pl-10 pr-8 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white min-w-[200px]"
                >
                  <option value="">All Countries</option>
                  {countries.map(country => (
                    <option key={country} value={country}>{country}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Destinations Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredDestinations.map(destination => (
                <DestinationCard
                  key={destination.id}
                  destination={destination}
                  onSelect={handleDestinationSelect}
                />
              ))}
            </div>

            {filteredDestinations.length === 0 && (
              <div className="text-center py-12">
                <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No destinations found</h3>
                <p className="text-gray-600">Try adjusting your search or filter criteria</p>
              </div>
            )}
          </div>
        ) : (
          <div>
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">My Trip Plans</h2>
              <p className="text-gray-600">Manage and track your planned adventures</p>
            </div>

            {trips.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {trips.map(trip => (
                  <TripCard
                    key={trip.id}
                    trip={trip}
                    onDelete={handleTripDelete}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="bg-gray-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <MapPin className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No trips planned yet</h3>
                <p className="text-gray-600 mb-4">Start exploring destinations to create your first trip plan</p>
                <button
                  onClick={() => setActiveTab('explore')}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200"
                >
                  Explore Destinations
                </button>
              </div>
            )}
          </div>
        )}
      </main>

      {selectedDestination && (
        <TripPlanningModal
          destination={selectedDestination}
          isOpen={isModalOpen}
          onClose={handleModalClose}
          onSave={handleTripSave}
        />
      )}
    </div>
  );
}

export default App;