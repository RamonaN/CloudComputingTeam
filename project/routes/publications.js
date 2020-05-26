var express = require('express');
var router = express.Router();

publishController = require('../controllers/publishController');

router.get('/', function(req, res, next) {
  if (!req.isAuthenticated())
    return res.redirect('/');

  const userId = req.user.profile.id;

  publishController.getPublicationsByUser(userId, (err, publicari) => {
    if (err) 
    {
      return next(err);
    }
    
    res.render('publications',{'publish': publicari});
  });

});

module.exports=router;