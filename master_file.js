const fs = require('fs');
const path = require('path');

// Directory where the JSON files are stored
const jsonDir = './json&html_files';
const masterFile = 'master_file.json';

// Initialize an empty array to store the merged content
let masterData = [];

// Function to read and merge all JSON files
fs.readdir(jsonDir, (err, files) => {
  if (err) {
    return console.error('Unable to scan directory:', err);
  }

  // Filter to only include .json files
  files = files.filter(file => path.extname(file) === '.json');

  files.forEach((file, index) => {
    const filePath = path.join(jsonDir, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    // Add file content to the master data array
    masterData.push(data);

    // If it's the last file, write the combined data to the master JSON file
    if (index === files.length - 1) {
      fs.writeFileSync(masterFile, JSON.stringify(masterData, null, 2), 'utf8');
      console.log('Master JSON file created:', masterFile);
    }
  });
});
