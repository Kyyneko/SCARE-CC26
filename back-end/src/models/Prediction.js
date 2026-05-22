const { DataTypes } = require("sequelize");
const sequelize = require("../config/database");

const Prediction = sequelize.define("Prediction", {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true,
  },
  sessionId: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  label: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  accuracy: {
    type: DataTypes.STRING,
    allowNull: false,
  },
}, {
  timestamps: true, // Mengaktifkan createdAt dan updatedAt otomatis
});

module.exports = Prediction;
