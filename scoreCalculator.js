// backend/scoreCalculator.js
import { getFmrByFips } from "./FMR/fmrService.js";
//These need to call the users data after a personality quiz! FOR FMR SCORING
let Cheap = 0;
let Moderate = 0;
let Costly = 0;
let Luxury = 0;

//These are the avg values for goal FMR 
let avgCheap = 500;
let avgModerate = 1000;
let avgCostly = 1500;
let avgLuxury = 2000;
let FMRlimit = 1000;//scaling for the fmr scores


/**
 * Calculate a cost-of-living score
 * @param {string} fipsCode - 10-digit FIPS code
 * @returns {Promise<{ score: number, oneBedroom: number, twoBedroom: number }>}
 */
async function calculateScore(fipsCode) {
    try {
        // Get FMR data
        const fmr = await getFmrByFips(fipsCode);

        // Simple scoring formula (adjust weights as soon as user data in)
        const averageRent = (fmr.oneBedroom + fmr.twoBedroom) / 2;
        //user FMR is the goal FMR of user based on their quiz results
        const userFMR = (Costly * avgCheap + Moderate * avgModerate + Cheap * avgCostly + Luxury * avgLuxury) / (Costly + Moderate + Cheap + Luxury);
        const difference = Math.abs(userFMR - averageRent); // Absolute difference between user and average rent
        const score = 10 - ((difference / FMRlimit) * 10); // 10/10 score


        return {
            score: Math.round(score),
        };
    } catch (error) {
        console.error('Score calculation failed:', error.message);
        throw error; // Re-throw for caller to handle
    }
}

// Example usage
(async () => {
    const denverScore = await calculateScore('0801499999'); // Denver FIPS
    console.log(denverScore);
})();

export default { calculateScore };