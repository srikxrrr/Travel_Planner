export interface Destination {
  id: string;
  name: string;
  country: string;
  description: string;
  imageUrl: string;
  estimatedCost: number;
  bestTimeToVisit: string;
  activities: string[];
}

export interface Trip {
  id: string;
  destination: Destination;
  startDate: Date;
  endDate: Date;
  budget: number;
  travelers: number;
  notes: string;
  status: 'planned' | 'booked' | 'completed';
}

export interface TravelPlan {
  id: string;
  title: string;
  trips: Trip[];
  totalBudget: number;
  createdAt: Date;
  updatedAt: Date;
}