const prisma = require("../models/db");
const { setPassword, generateJWT } = require("../models/users");
const passport = require("passport");

const register = async (req, res) => {
  if (!req.body.name || !req.body.email || !req.body.password) {
    return res.status(400).json({ message: "All fields required" });
  }

  const { salt, hash } = setPassword(req.body.password);

  try {
    const user = await prisma.user.create({
      data: {
        name: req.body.name,
        email: req.body.email,
        salt: salt,
        hash: hash,
      },
    });

    const token = generateJWT(user);
    return res.status(200).json({ token });
  } catch (err) {
    return res.status(400).json(err);
  }
};

const login = (req, res) => {
  if (!req.body.email || !req.body.password) {
    return res.status(400).json({ message: "All fields required" });
  }

  passport.authenticate("local", (err, user, info) => {
    if (err) {
      return res.status(404).json(err);
    }

    if (user) {
      const token = generateJWT(user);
      res.status(200).json({ token });
    } else {
      res.status(401).json(info);
    }
  })(req, res);
};

module.exports = {
  register,
  login,
};
