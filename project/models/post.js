module.exports.modelPost = (columns) => {
  var post = {};
  post.utilizator = columns[0].value;
  post.titlu = columns[1].value;
  post.descriere = columns[2].value;
  post.dataPostarii = columns[3].value;
  return post;
}