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

  // Load trips from localStorage on component mount
  useEffect(() => {
    const savedTrips = localStorage.getItem('travelPlannerTrips');
    if (savedTrips) {
      const parsedTrips = JSON.parse(savedTrips).map((trip: any) => ({
        ...trip,
        startDate: new Date(trip.startDate),
        endDate: new Date(trip.endDate),
      }));
      setTrips(parsedTrips);
    }
  }, []);

  // Save trips to localStorage whenever trips change
  useEffect(() => {
    localStorage.setItem('travelPlannerTrips', JSON.stringify(trips));
  }, [trips]);

  const handleDestinationSelect = (destination: Destination) => {
    setSelectedDestination(destination);
    setIsModalOpen(true);
  };

  const handleTripSave = (tripData: Omit<Trip, 'id'>) => {
    const newTrip: Trip = {
      ...tripData,
      id: Date.now().toString(),
    };
    setTrips(prev => [...prev, newTrip]);
    setActiveTab('trips');
  };

  const handleTripDelete = (tripId: string) => {
    setTrips(prev => prev.filter(trip => trip.id !== tripId));
  };

  const filteredDestinations = destinations.filter(destination => {
    const matchesSearch = destination.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         destination.country.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCountry = !selectedCountry || destination.country === selectedCountry;
    return matchesSearch && matchesCountry;
  });

  const countries = [...new Set(destinations.map(d => d.country))].sort();

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        activeTab={activeTab} 
        onTabChange={setActiveTab} 
        tripCount={trips.length}
      />

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
          onClose={() => setIsModalOpen(false)}
          onSave={handleTripSave}
        />
      )}
    </div>
  );
}

export default App;