import React, { useState } from 'react';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { TripPlanningForm } from './components/TripPlanningForm';
import { TripResults } from './components/TripResults';
import { FeaturedDestinations } from './components/FeaturedDestinations';
import { Footer } from './components/Footer';

export interface TripPlan {
  id: string;
  destination: string;
  duration: number;
  travelers: number;
  budget: string;
  interests: string[];
  itinerary: Array<{
    day: number;
    title: string;
    activities: Array<{
      time: string;
      activity: string;
      description: string;
      cost?: string;
    }>;
  }>;
  estimatedCost: {
    accommodation: number;
    food: number;
    activities: number;
    transport: number;
    total: number;
  };
}

function App() {
  const [currentTripPlan, setCurrentTripPlan] = useState<TripPlan | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleTripGenerated = (tripPlan: TripPlan) => {
    setCurrentTripPlan(tripPlan);
  };

  const handleNewTrip = () => {
    setCurrentTripPlan(null);
  };

  return (
    <div className="min-h-screen bg-white">
      <Header onNewTrip={handleNewTrip} />
      
      {!currentTripPlan ? (
        <>
          <Hero />
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 -mt-16 relative z-10">
            <TripPlanningForm 
              onTripGenerated={handleTripGenerated}
              isGenerating={isGenerating}
              setIsGenerating={setIsGenerating}
            />
          </div>
          <FeaturedDestinations />
        </>
      ) : (
        <TripResults tripPlan={currentTripPlan} onNewTrip={handleNewTrip} />
      )}
      
      <Footer />
    </div>
  );
}

export default App;