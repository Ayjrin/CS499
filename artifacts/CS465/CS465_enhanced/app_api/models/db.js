const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

// Configure for Graceful Shutdown
const gracefulShutdown = async (msg) => {
  await prisma.$disconnect();
  console.log(`Prisma disconnected through ${msg}`);
};

// Event Listeners to process graceful shutdowns
// Shutdown invoked by nodemon signal
process.once("SIGUSR2", async () => {
  await gracefulShutdown("nodemon restart");
  process.kill(process.pid, "SIGUSR2");
});

// Shutdown invoked by app termination
process.on("SIGINT", async () => {
  await gracefulShutdown("app termination");
  process.exit(0);
});

// Shutdown invoked by container termination
process.on("SIGTERM", async () => {
  await gracefulShutdown("app shutdown");
  process.exit(0);
});

module.exports = prisma;
