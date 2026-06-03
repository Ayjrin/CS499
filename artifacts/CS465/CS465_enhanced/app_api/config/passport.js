const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const prisma = require("../models/db");
const { validPassword } = require("../models/users");

passport.use(
  new LocalStrategy(
    {
      usernameField: "email",
    },
    async (username, password, done) => {
      try {
        const user = await prisma.user.findUnique({
          where: { email: username },
        });

        if (!user) {
          return done(null, false, {
            message: "Incorrect user name.",
          });
        }

        if (!validPassword(password, user.salt, user.hash)) {
          return done(null, false, {
            message: "Incorrect password.",
          });
        }

        return done(null, user);
      } catch (err) {
        return done(err);
      }
    },
  ),
);
