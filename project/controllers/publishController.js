const createError = require('http-errors');
const { Request } = require("tedious");
const { modelPublication } = require("../models/publication")
const connection = require("../database/connection");

module.exports.getPublicationsByUser = (userId, next) => {

  const request = new Request(
    `SELECT *
     FROM [dbo].[Publicari] 
     WHERE utilizator = '${userId}'`,
    (err, rowCount) => {
      if (err) {
        next(createError(500, err.message));
      } else {
        console.log(`${rowCount} row(s) returned`);
      }
    }
  );

  var publicari = [];
  request.on("row", columns => {
    var publicare = modelPublication(columns);
    publicari.push(publicare)
  });

  request.on("err", err => {
    next(createError(500, err.message));
  });

  request.on('requestCompleted', () => { 
    next(undefined, publicari);
  });

  connection.execSql(request);
}