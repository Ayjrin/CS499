const crypto = require("crypto");
const jwt = require("jsonwebtoken");

// Helper to set the password (generate salt and hash)
const setPassword = (password) => {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto
    .pbkdf2Sync(password, salt, 1000, 64, "sha512")
    .toString("hex");
  return { salt, hash };
};

// Helper to compare entered password against stored hash
const validPassword = (password, salt, storedHash) => {
  const hash = crypto
    .pbkdf2Sync(password, salt, 1000, 64, "sha512")
    .toString("hex");
  return storedHash === hash;
};

// Helper to generate a JSON Web Token
const generateJWT = (user) => {
  return jwt.sign(
    {
      // Payload for our JSON Web Token
      _id: user.id,
      email: user.email,
      name: user.name,
    },
    process.env.JWT_SECRET, // SECRET stored in .env file
    { expiresIn: "1h" }, // Token expires an hour from creation
  );
};

module.exports = {
  setPassword,
  validPassword,
  generateJWT,
};
