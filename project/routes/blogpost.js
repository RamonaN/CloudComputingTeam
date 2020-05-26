var express = require('express');
var router = express.Router();

router.get('/',(req,res)=> {

  postController.getTopPosts((err, posts) => {
    res.render('blogposts.hbs', {'posts': posts});
  })
})

module.exports = router;