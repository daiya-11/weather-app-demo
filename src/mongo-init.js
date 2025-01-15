// Authenticate with root credentials
db.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD)

// Switch to the weather database
db = db.getSiblingDB('weather-db-staging')

// Create root user with readWrite access
db.createUser({
  user: process.env.MONGO_INITDB_ROOT_USERNAME,
  pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
  roles: [
    {
      role: 'readWrite',
      db: 'weather-db-staging'
    }
  ]
})

// Create app user with readWrite access
db.createUser({
  user: process.env.MONGO_USER,
  pwd: process.env.MONGO_PASSWORD,
  roles: [
    {
      role: 'readWrite',
      db: 'weather-db-staging'
    }
  ]
})