import React from "react";
import logo2 from "./../assets/logo2.png";

export default function SearchWindow() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-[#282c34]">
      <img src={logo2} alt="Google Logo" className="w-48 mb-6" />
      <div className="flex items-center justify-center">
        <input
          type="text"
          placeholder="Search Google"
          className="py-2 px-4 text-lg border border-gray-300 rounded-l-lg focus:outline-none focus:border-blue-500"
        />
        <button className="py-2 px-4 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 transition duration-300 focus:outline-none">
          Search
        </button>
      </div>
    </div>
  );
}
