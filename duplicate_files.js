const fs = require('fs');

// Function to find duplicates within a single array (case-insensitive)
const findDuplicatesWithinArray = (arr) => {
    const fileCount = {};
    const duplicates = [];

    // Count occurrences of each file name (case-insensitive)
    arr.forEach(file => {
        const lowerCaseFile = file.toLowerCase();
        if (fileCount[lowerCaseFile]) {
            fileCount[lowerCaseFile]++;
        } else {
            fileCount[lowerCaseFile] = 1;
        }
    });

    // Collect duplicates
    for (const [file, count] of Object.entries(fileCount)) {
        if (count > 1) {
            duplicates.push(file); // Store the duplicate in lowercase
        }
    }

    // Return duplicates with original casing from the array
    return duplicates.map(file => arr.find(original => original.toLowerCase() === file));
};

// Function to find duplicates between two arrays (case-insensitive)
const findDuplicatesBetweenStores = (arr1, arr2) => {
    const store1Lower = arr1.map(file => file.toLowerCase());
    const store2Lower = arr2.map(file => file.toLowerCase());
    
    const duplicates = store1Lower.filter(file => store2Lower.includes(file));
    
    return duplicates.map(file => {
        // Return the duplicates with their original casing from the first store
        return arr1.find(original => original.toLowerCase() === file);
    });
};

// Function to read Play Store CSV file (comma-separated)
const readPlayStoreCSV = (filePath) => {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return reject(err);
            }
            // Split by new lines, then extract the second column (app name) from comma-separated values
            const apps = data
                .split('\n')
                .map(line => line.split(',')[1]) // Only get the app name part after comma
                .filter(app => app); // Filter out undefined or empty entries
            resolve(apps);
        });
    });
};

// Function to read Apple Store CSV file (no commas)
const readAppleStoreCSV = (filePath) => {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return reject(err);
            }
            // Split by new lines and trim whitespace
            const apps = data
                .split('\n')
                .map(app => app.trim()) // Just take each line as is
                .filter(app => app); // Filter out any empty entries
            resolve(apps);
        });
    });
};

// Main function to process the files and find duplicates
const processFiles = async () => {
    try {
        // Read Play Store and Apple Store CSV files
        const playStoreApps = await readPlayStoreCSV('./app_store_scraper/playstore_scraper/apps_names.csv');
        const appleStoreApps = await readAppleStoreCSV('./app_store_scraper/apple_apps.csv');

        // Find duplicates within each store
        const playStoreDuplicates = findDuplicatesWithinArray(playStoreApps);
        const appleStoreDuplicates = findDuplicatesWithinArray(appleStoreApps);

        // Find duplicates between Play Store and Apple Store
        const duplicateBetweenStores = findDuplicatesBetweenStores(playStoreApps, appleStoreApps);

        // Output the results
        if (playStoreDuplicates.length > 0) {
            console.log("Duplicate Apps within Play Store:");
            playStoreDuplicates.forEach(app => console.log(app));
        } else {
            console.log("No duplicates in Play Store.\n");
        }

        if (appleStoreDuplicates.length > 0) {
            console.log("\nDuplicate Apps within Apple Store:");
            appleStoreDuplicates.forEach(app => console.log(app));
        } else {
            console.log("No duplicates in Apple Store.\n");
        }

        if (duplicateBetweenStores.length > 0) {
            console.log("Duplicate Apps found in both Play Store and Apple Store:");
            duplicateBetweenStores.forEach(app => console.log(app));
        } else {
            console.log("\nNo duplicate apps found between Play Store and Apple Store.");
        }

    } catch (error) {
        console.error("Error processing files:", error);
    }
};

// Run the process
processFiles();
