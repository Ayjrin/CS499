let express = require('express');
let router = express.Router();
let controller = require('../controllers/travel');

router.get('/', controller.travel);

module.exports = router;

