let express = require('express');
let router = express.Router();
let controller = require('../controllers/users');

router.get('/', controller.users);

module.exports = router;

