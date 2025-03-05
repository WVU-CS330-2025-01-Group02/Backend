async function fetchWalkabilityData() {
    document.getElementById("loading").style.display = "block";
    
    try {
        const response = await fetch("http://localhost:5000/api/walkability");
        if (!response.ok) throw new Error("Failed to fetch data");

        const data = await response.json();
        const tableBody = document.querySelector("#walkability-table tbody");
        tableBody.innerHTML = ""; // Clear existing data

        data.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.state_fips}</td>
                <td>${row.county_fips}</td>
                <td>${row.intersection_density}</td>
                <td>${row.proximity_to_transit}</td>
                <td>${row.employment_mix}</td>
                <td>${row.employment_household_mix}</td>
                <td>${row.walkability_index}</td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (error) {
        alert("Error fetching data: " + error.message);
    } finally {
        document.getElementById("loading").style.display = "none";
    }
}

// Fetch data on page load
fetchWalkabilityData();
