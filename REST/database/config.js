module.exports = config = {
  authentication: {
    options: {
      userName: "book-storage",
      password: "<password>"
    },
    type: "default"
  },
  server: "book-storage.database.windows.net",
  options: {
    database: "BookDB",
    encrypt: true
  }
};
