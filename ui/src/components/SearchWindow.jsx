import React, { useState } from "react";
import axios from "axios";
import logo2 from "./../assets/logo2.png";
import { SearchResult } from "./SearchResult";
import NewDoc from "./NewDoc";

export default function SearchWindow() {
  const [query, setQuery] = useState("");
  const [duration, setDuration] = useState(0.0);
  const [results, setResults] = useState([]);

  const handleSearch = () => {
    axios
      .get("http://localhost:5000/search", {
        params: {
          query: query.toString(),
        },
      })
      .then((response) => {
        setResults(response.data.results);
        setDuration(response.data.duration);
      })
      .catch((error) => {
        console.error("Error fetching results:", error);
      });
  };

  return (
    <div className="flex-1 flex-col items-center justify-center h-screen overflow-y-scroll">
      <div className="h-1/4 w-full bg-[#092635] py-8 px-4">
        <img
          src={logo2}
          alt="Google Logo"
          className="w-48 mb-6 mx-auto logo bg-transparent"
        />
        <div className="flex flex-row justify-center">
          <div className="flex items-center justify-center mr-6">
            <input
              type="text"
              placeholder="Search Google"
              className="py-2 px-4 text-lg border border-gray-300 rounded-l-lg focus:outline-none focus:border-blue-500"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button
              className="py-3 px-4 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 transition duration-300 focus:outline-none"
              onClick={handleSearch}
            >
              Search
            </button>
          </div>
          <button className="bg-purple-50 p-3 rounded-lg">
            <NewDoc />
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto mt-[calc(50vh + 4rem)] w-full">
        <div className="flex justify-start items-center bg-slate-400 px-8">
          <h1 className="font-bold text-black text-xl">
            {results.length} results in {duration.toFixed(2)} sec duration
          </h1>
        </div>
        <div className="bg-slate-400 py-8 px-4">
          {results.map((result, index) => (
            <SearchResult
              key={index}
              pageTitle={result.title}
              url={result.url}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
