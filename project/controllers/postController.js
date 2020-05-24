const createError = require('http-errors');
const { Request } = require("tedious");
const { modelPost } = require("../models/review")
const connection = require("../database/connection");

module.exports.getPostsByUser = (userId, next) => {

  const request = new Request(
    `SELECT *
     FROM [dbo].[Postari] 
     WHERE utilizator = '${userId}'`,
    (err, rowCount) => {
      if (err) {
        next(createError(500, err.message));
      } else {
        console.log(`${rowCount} row(s) returned`);
      }
    }
  );

  var posts = [];
  request.on("row", columns => {
    var post = modelPost(columns);
    posts.push(post)
  });

  request.on("err", err => {
    next(createError(500, err.message));
  });

  request.on('requestCompleted', () => { 
    next(undefined, posts);
  });

  connection.execSql(request);
}