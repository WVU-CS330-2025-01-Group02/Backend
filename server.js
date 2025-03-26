const express = require("express");
const axios = require("axios");
const cors = require("cors");
const fs = require("fs");
const csv = require("fast-csv");

const app = express();
const PORT = process.env.PORT || 3000;
const PROCESSED_WALKABILITY_FILE = "walkability_index_processed.csv";
const GAZETTEER_FILE = "2024_Gaz_place_national_processed.csv";

let walkabilityData = [];
let cityMapping = {}; // will store GEOID to city mapping

// load walkability data
function loadWalkabilityData() {
    return new Promise((resolve, reject) => {
        let data = [];
        fs.createReadStream(PROCESSED_WALKABILITY_FILE)
            .pipe(csv.parse({ headers: true }))
            .on("data", (row) => {
                data.push(row);
            })
            .on("end", () => {
                walkabilityData = data;
                resolve();
            })
            .on("error", reject);
    });
}

// load gazetter (for place_name to GEOID mapping)
function loadCityMapping() {
    return new Promise((resolve, reject) => {
        fs.createReadStream(GAZETTEER_FILE)
            .pipe(csv.parse({ headers: true}))
            .on("data", (row) => {
                cityMapping[row.NAME.toLowerCase()] = row.GEOID;
            })
            .on("end", resolve)
            .on("error", reject);
    });
}

// API endpoint to get walkability data by place name
app.get("/api/walkability", async (req, res) => {
    const { place_name } = req.query;

    if (!place_name) {
        return res.status(400).json({ error: "Place name parameter is required" });
    }

    const placeNameLower = place_name.toLowerCase();

    const geoid = cityMapping[placeNameLower];

    if (!geoid) {
        return res.status(404).json({ error: "City not found for this place name" });
    }

    const results = walkabilityData.filter((row) => row.GEOID_12digit === geoid);

    if (results.length === 0) {
        return res.status(404).json({ error: "Walkability data not found for this GEOID" });
    }

    res.json(results);
});

// start server
async function startServer() {
    try {
        console.log("Loading datasets...");
        await loadWalkabilityData();
        await loadCityMapping();
        console.log("Datasets loaded. Starting server...");

        app.listen(PORT, () => {
            console.log(`Server running on http://localhost:${PORT}`);
        });
    } catch (error) {
        console.error("Error loading datasets: ", error);
    }
}

startServer();