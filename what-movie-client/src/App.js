import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Create an instance of Axios with the base URL
    const api = axios.create({
      baseURL: "http://localhost:5000",
    });
    const fetchData = async () => {
      try {
        const response = await api.get("/api/data");
        console.log(response.data);
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {data ? (
        <div>
          <h1>{data.message}</h1>
          <p>Number: {data.number}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default App;
