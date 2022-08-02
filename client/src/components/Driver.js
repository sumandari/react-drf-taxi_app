import React, {useState, useEffect} from 'react';
import { Breadcrumb, Card } from 'react-bootstrap';
import { Navigate } from 'react-router-dom';


import TripCard from './TripCard';
import { isDriver } from '../services/AuthService';
import { getTrips } from '../services/TripService';

function Driver(props) {
  const [trips, setTrips] = useState([]);
  const getCurrentTrips = () => {
    return trips.filter(trip => {
      return (
        trip.rider !== null &&
        trip.status !== 'REQUESTED' &&
        trip.status !== 'COMPLETED'
      );
    });
  };

  const getRequestedTrips = () => {
    return trips.filter(trip => { 
      return trip.status === 'REQUESTED';
    })
  }
  
  const getCompletedTrips = () => {
    return trips.filter(trip => { 
      return trip.status === 'COMPLETED'
    });
  };
  
  useEffect(() => {
    const loadTrips = async () => {
      const { response, isError } = await getTrips();
      if (isError) {
        setTrips([])
      } else {
        setTrips(response.data);
      }
    };
    loadTrips();
  }, []);

  if (!isDriver()) {
    return <Navigate to='/' />;
  }
  return (
    <>
      <Breadcrumb>
        <Breadcrumb.Item href='/'>Home</Breadcrumb.Item>
        <Breadcrumb.Item active>Dashboard</Breadcrumb.Item>
      </Breadcrumb>
      <TripCard
        title='Current Trip'
        trips={getCurrentTrips()}
        group='driver'
        otherGroup='rider'
      />
      <TripCard
        title='Requested Trip'
        trips={getRequestedTrips()}
        group='driver'
        otherGroup='rider'
      />
      <TripCard
        title='Recent Trips'
        trips={getCompletedTrips()}
        group='driver'
        otherGroup='rider'
      />
    </>
  );
}

export default Driver;
