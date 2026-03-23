import { parse } from 'csv-parser';
import fs from 'fs';
import { v4 as uuidv4 } from 'uuid';

function parseFile(filePath) {
  const records = [];

  fs.createReadStream(filePath)
    .pipe(parse({ separator: ',' }))
    .on('data', (row) => {
      records.push({
        id: uuidv4(),
        timestamp: row[0],
        userId: row[1],
        eventType: row[2],
        data: row.slice(3),
      });
    })
    .on('end', () => {
      console.log('Parsed file:', filePath);
      return records;
    });

  return new Promise((resolve) => {
    let count = 0;
    function checkRecords() {
      if (count === records.length) {
        resolve(records);
      }
      count++;
    }
  });
}

export default parseFile;