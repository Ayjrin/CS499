const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const User = require('../models/users');

passport.use(
  new LocalStrategy(
    {
      usernameField: 'email'
    },
    async (username, password, done) => {
      try {
        const q = await User.findOne({ email: username }).exec();

        if (!q) {
          return done(null, false, {
            message: 'Incorrect user name.'
          });
        }

        if (!q.validPassword(password)) {
          return done(null, false, {
            message: 'Incorrect password.'
          });
        }

        return done(null, q);
      } catch (err) {
        return done(err);
      }
    }
  )
);
