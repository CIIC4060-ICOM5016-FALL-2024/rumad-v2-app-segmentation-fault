from flask import jsonify, request
from dao.registration import RegistrationDAO

class RegistrationHandler:
  def mapToDict(self, tuple):
    result = {}
    result["username"] = tuple[0]
    result["password"] = tuple[1]
    return result
  
  def logInUser(self, username, password):
      if not username or not password:
          return jsonify(Error="Username and password are required"), 400
      dao = RegistrationDAO()
      result = dao.logInUser(username, password)
      if result is None:
          return jsonify(Error="User not found"), 404
      else:
          return jsonify(User=self.mapToDict(result)), 200

  def signUpUser(self, username, password):
          if not username or not password:
              return jsonify(Error="Username and password are required"), 400
          dao = RegistrationDAO()
          try:
              result = dao.signUpUser(username, password)
              return jsonify(User={"username": result}), 201
          except ValueError as ve:
              return jsonify(Error=str(ve)), 409  # Código 409: Conflict
          except Exception as e:
              return jsonify(Error="An unexpected error occurred."), 500
