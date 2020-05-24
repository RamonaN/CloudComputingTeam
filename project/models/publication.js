module.exports.modelPublication = (columns) => {
  var publication = {};
  publication.utilizator = columns[0].value;
  publication.titlu = columns[1].value;
  publication.descriere = columns[2].value;
  publication.continut = columns[3].value;
  publication.etapa = columns[4].value;
  return publication;
}