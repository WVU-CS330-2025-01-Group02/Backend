const express = require("express");
const cors = require("cors");
const axios = require("axios");
const Papa = require("papaparse");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());

// API endpoint to fetch and parse CSV data
app.get("/api/walkability", async (req, res) => {
    try {
        const csvUrl = "https://edg.epa.gov/EPADataCommons/public/OA/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv";
        const response = await axios.get(csvUrl, { responseType: "text" });

        Papa.parse(response.data, {
            header: true,
            skipEmptyLines: true,
            complete: (result) => {
                // Extract relevant data (limiting to first 10 rows)
                const filteredData = result.data.slice(0, 10).map(row => ({
                    state_fips: row["STATEFP"] || "N/A",
                    county_fips: row["COUNTYFP"] || "N/A",
                    intersection_density: row["D3B_Ranked"] || "N/A",
                    proximity_to_transit: row["D4A_Ranked"] || "N/A",
                    employment_mix: row["D2B_Ranked"] || "N/A",
                    employment_household_mix: row["D2A_Ranked"] || "N/A",
                    walkability_index: row["NatWalkInd"] || "N/A"
                }));

                res.json(filteredData);
            }
        });
    } catch (error) {
        res.status(500).json({ error: "Failed to fetch data" });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
