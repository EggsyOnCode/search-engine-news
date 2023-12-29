import React, { useState } from "react";
import axios from "axios";
import logo2 from "./../assets/logo2.png";
import { SearchResult } from "./SearchResult";
import NewDoc from "./NewDoc";
import { SearchSharp } from "react-ionicons";

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
    <div className="flex-1 flex-col items-center justify-center h-screen overflow-y-scroll w-full">
      <div className="flex flex-row justify-around items-center">
        <div className="h-1/4 w-full bg-purple-50 py-8 px-4">
          <img
            src={logo2}
            alt="Google Logo"
            className="w-48 mb-6 mx-auto logo bg-transparent"
          />
          <div className="flex flex-row justify-center w-full">
            <form
            className="w-full"
              onSubmit={(e) => {
                e.preventDefault(); // Prevent default form submission
                handleSearch(); // Call the handleSearch function on form submission
              }}
            >
              <div className="flex items-center justify-center mr-6 w-full">
                <input
                  type="text"
                  placeholder="Search Google"
                  className="w-1/2 py-2 px-4 text-lg border border-gray-300 rounded-l-lg focus:outline-none focus:border-blue-500"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <button
                  type="submit" // Set button type to submit
                  className="py-3 px-4 bg-pink-400 text-white rounded-r-lg hover:bg-pink-600 transition duration-300 focus:outline-none"
                >
                  <SearchSharp color={"#00000"} />
                </button>
              </div>
            </form>
            <button className="fixed top-26 left-5 bg-pink-300 p-3 rounded-lg text-black font-extrabold">
              <NewDoc />
            </button>
          </div>
        </div>
      </div>
      <div className="rounded-lg flex-1 overflow-y-auto mt-[calc(50vh + 4rem)] px-40 mt-6">
        <div className="bg-[#47BE41] py-8 px-4 rounded-lg">
          <h1 className="text-3xl mb-2">Search Results</h1>
          <hr className="border-black border-r-8" />
          <h1 className="font-normal text-black text-xl">
            {results.length} results in {duration.toFixed(2)} sec duration
          </h1>
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
