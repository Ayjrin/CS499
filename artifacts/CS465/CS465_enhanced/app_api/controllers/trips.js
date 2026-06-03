const prisma = require("../models/db");

const tripsList = async (req, res) => {
  try {
    const q = await prisma.trip.findMany();
    return res.status(200).json(q);
  } catch (err) {
    return res
      .status(404)
      .json({ message: "Error retrieving trips", error: err });
  }
};

const tripsFindByCode = async (req, res) => {
  try {
    const q = await prisma.trip.findUnique({
      where: { code: req.params.tripCode },
    });

    if (!q) {
      return res.status(404).json({ message: "Trip not found" });
    } else {
      return res.status(200).json(q);
    }
  } catch (err) {
    return res.status(400).json({ message: "Error finding trip", error: err });
  }
};

const tripsAddTrip = async (req, res) => {
  try {
    const q = await prisma.trip.create({
      data: {
        code: req.body.code,
        name: req.body.name,
        length: req.body.length,
        start: new Date(req.body.start),
        resort: req.body.resort,
        perPerson: req.body.perPerson,
        image: req.body.image,
        description: req.body.description,
      },
    });
    return res.status(201).json(q);
  } catch (err) {
    return res.status(400).json({ message: "Error adding trip", error: err });
  }
};

const tripsUpdateTrip = async (req, res) => {
  try {
    const q = await prisma.trip.update({
      where: { code: req.params.tripCode },
      data: {
        code: req.body.code,
        name: req.body.name,
        length: req.body.length,
        start: new Date(req.body.start),
        resort: req.body.resort,
        perPerson: req.body.perPerson,
        image: req.body.image,
        description: req.body.description,
      },
    });
    return res.status(201).json(q);
  } catch (err) {
    return res.status(400).json({ message: "Error updating trip", error: err });
  }
};

module.exports = {
  tripsList,
  tripsFindByCode,
  tripsAddTrip,
  tripsUpdateTrip,
};
