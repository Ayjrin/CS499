const prisma = require("./db");
const fs = require("fs");
const path = require("path");

// Adjusted path to find trips.json relative to this file or the project root
const tripsPath = path.join(__dirname, "../../data/trips.json");
const trips = JSON.parse(fs.readFileSync(tripsPath, "utf8"));

const seedDB = async () => {
  console.log("Cleaning up existing trips...");
  await prisma.trip.deleteMany({});

  console.log("Seeding trips...");
  for (const trip of trips) {
    await prisma.trip.create({
      data: {
        code: trip.code,
        name: trip.name,
        length: trip.length,
        start: new Date(trip.start),
        resort: trip.resort,
        perPerson: trip.perPerson,
        image: trip.image,
        description: trip.description,
      },
    });
  }
  console.log("Seeding complete.");
};

seedDB()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
    process.exit(0);
  });
