import React from 'react';
import { Link } from 'react-router-dom';

const MainDashboard = () => {
  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 font-poppins px-6 py-10">
      <h1 className="text-5xl font-extrabold text-gray-900 text-center mt-8 mb-12">
        Check-in System
      </h1>

      <div className="flex flex-col gap-6 w-full max-w-md ">
        <Link to="/checkin">
          <button className="w-full bg-green-600 hover:bg-green-700 text-white rounded-lg text-2xl font-semibold py-6 transition-all duration-300 transform hover:scale-105 shadow-md hover:shadow-lg">
            Check-In
          </button>
        </Link>


        <Link to="/checkin-visitor">
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-2xl font-semibold py-6 transition-all duration-300 transform hover:scale-105 shadow-md hover:shadow-lg">
            Visitor Check-In
          </button>
        </Link>
      </div>
    </div>
  );
};

export default MainDashboard;
