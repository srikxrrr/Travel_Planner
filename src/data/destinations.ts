import { Destination } from '../types';

export const destinations: Destination[] = [
  {
    id: '1',
    name: 'Tokyo',
    country: 'Japan',
    description: 'A vibrant metropolis blending traditional culture with cutting-edge technology.',
    imageUrl: 'https://images.pexels.com/photos/2506923/pexels-photo-2506923.jpeg?auto=compress&cs=tinysrgb&w=800',
    estimatedCost: 3500,
    bestTimeToVisit: 'March-May, September-November',
    activities: ['Temple visits', 'Sushi tasting', 'Shopping in Shibuya', 'Cherry blossom viewing']
  },
  {
    id: '2',
    name: 'Paris',
    country: 'France',
    description: 'The City of Light, famous for its art, fashion, gastronomy, and culture.',
    imageUrl: 'https://images.pexels.com/photos/338515/pexels-photo-338515.jpeg?auto=compress&cs=tinysrgb&w=800',
    estimatedCost: 2800,
    bestTimeToVisit: 'April-June, September-October',
    activities: ['Eiffel Tower', 'Louvre Museum', 'Seine River cruise', 'Café culture']
  },
  {
    id: '3',
    name: 'Bali',
    country: 'Indonesia',
    description: 'Tropical paradise known for its beaches, temples, and vibrant culture.',
    imageUrl: 'https://images.pexels.com/photos/2474690/pexels-photo-2474690.jpeg?auto=compress&cs=tinysrgb&w=800',
    estimatedCost: 1800,
    bestTimeToVisit: 'April-October',
    activities: ['Beach relaxation', 'Temple tours', 'Rice terrace hiking', 'Spa treatments']
  },
  {
    id: '4',
    name: 'New York City',
    country: 'USA',
    description: 'The Big Apple - a bustling metropolis with iconic landmarks and endless entertainment.',
    imageUrl: 'https://images.pexels.com/photos/466685/pexels-photo-466685.jpeg?auto=compress&cs=tinysrgb&w=800',
    estimatedCost: 4200,
    bestTimeToVisit: 'April-June, September-November',
    activities: ['Broadway shows', 'Central Park', 'Museums', 'Food tours']
  },
  {
    id: '5',
    name: 'Santorini',
    country: 'Greece',
    description: 'Stunning Greek island famous for its white-washed buildings and sunset views.',
    imageUrl: 'https://images.pexels.com/photos/1285625/pexels-photo-1285625.jpeg?auto=compress&cs=tinysrgb&w=800',
    estimatedCost: 2200,
    bestTimeToVisit: 'April-October',
    activities: ['Sunset watching', 'Wine tasting', 'Beach hopping', 'Photography']
  },
  {
    id: '6',
    name: 'Dubai',
    country: 'UAE',
    description: 'Modern city known for luxury shopping, ultramodern architecture, and nightlife.',
    imageUrl: 'https://images.pexels.com/photos/1470502/pexels-photo-1470502.jpeg?auto=compress&cs=tinysrgb&w=800',
    estimatedCost: 3200,
    bestTimeToVisit: 'November-March',
    activities: ['Burj Khalifa', 'Desert safari', 'Shopping malls', 'Beach resorts']
  }
];